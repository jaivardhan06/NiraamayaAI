import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini client setup
_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=_API_KEY) if _API_KEY else None
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def call_gemini(prompt: str, system: str, max_tokens: int = 1000) -> str:
    """Call Gemini and return its response text."""
    if client is None:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "system_instruction": system,
            "max_output_tokens": max_tokens,
            "temperature": 0.2,
        },
    )

    text = response.text
    if not text:
        raise ValueError("Gemini returned an empty response.")
    return text.strip()


def call_grok(prompt: str, system: str, max_tokens: int = 1000) -> str:
    """Backward-compatible wrapper; calls Gemini, not Grok."""
    return call_gemini(prompt, system, max_tokens)


def clean_json(text: str) -> str:
    """Remove Markdown code fences around JSON, if present."""
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            candidate = part.strip()
            if candidate.lower().startswith("json"):
                candidate = candidate[4:].strip()
            if candidate.startswith("{") or candidate.startswith("["):
                return candidate
    return text


def _parse_json_response(raw: str) -> Any:
    """Parse JSON, tolerating surrounding prose/code fences when possible."""
    cleaned = clean_json(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Best-effort extraction of the outermost JSON object/array.
        starts = [i for i in (cleaned.find("{"), cleaned.find("[")) if i >= 0]
        if not starts:
            raise
        start = min(starts)
        end_obj = cleaned.rfind("}")
        end_arr = cleaned.rfind("]")
        end = max(end_obj, end_arr)
        if end < start:
            raise
        return json.loads(cleaned[start : end + 1])


def extract_parameters(text: str) -> list:
    """Extract numeric health parameters from laboratory-report text as JSON."""
    system = (
        "You extract laboratory data faithfully. Return only a valid JSON array, "
        "with no explanation or Markdown. Do not infer values that are not present."
    )
    prompt = f"""Extract numeric health parameters from this lab report.

Return ONLY a JSON array in this format:
[
  {{
    "name": "parameter name from report",
    "key": "normalized_key_lowercase",
    "value": 12.5,
    "unit": "g/dL",
    "reference_range": "13.0-17.0"
  }}
]

Rules:
- value must be a number, not a string
- key must be lowercase with underscores
- Skip parameters without a numeric result
- Do not invent missing units or reference ranges; use an empty string if absent
- Keep the name as close as possible to the report's wording
- Extract each distinct numeric lab parameter only once

Key mapping examples:
- Haemoglobin / Hemoglobin -> hemoglobin
- TSH / T.S.H -> tsh
- Fasting Blood Sugar -> glucose_fasting
- Vitamin D / Vit D -> vitamin_d
- Vitamin B12 / Vit B12 -> vitamin_b12
- Serum Ferritin -> ferritin
- SGPT / ALT -> alt
- SGOT / AST -> ast
- Total Cholesterol -> total_cholesterol
- Triglycerides / TG -> triglycerides
- Uric Acid -> uric_acid
- Serum Creatinine -> creatinine

Lab report text:
{text[:12000]}"""

    try:
        raw = call_gemini(prompt, system, max_tokens=2500)
        result = _parse_json_response(raw)
        if not isinstance(result, list):
            raise ValueError("Expected a JSON array of parameters.")
        # Keep only entries that have the expected basic fields and numeric values.
        valid = []
        for item in result:
            if not isinstance(item, dict):
                continue
            try:
                value = float(item.get("value"))
            except (TypeError, ValueError):
                continue
            name = str(item.get("name", "")).strip()
            key = str(item.get("key", "")).strip().lower()
            if not name or not key:
                continue
            item["value"] = value
            item["unit"] = str(item.get("unit") or "")
            item["reference_range"] = str(item.get("reference_range") or "")
            valid.append(item)
        print(f"Extracted {len(valid)} parameters")
        return valid
    except Exception as exc:
        print(f"Parameter extraction failed: {exc}")
        return []


def generate_explanation(
    name: str,
    value: float,
    unit: str,
    status: str,
    min_val: float,
    max_val: float,
) -> dict:
    """Generate a simple English and Hindi explanation for one lab parameter."""
    system = (
        "You are NiraamayaAI, a cautious health-information assistant for Indian users. "
        "Explain lab results simply, do not diagnose, and return only valid JSON."
    )
    prompt = f"""Explain this health parameter in simple language.

Parameter: {name}
Patient value: {value} {unit}
Status: {status}
Reference interval supplied by the app: {min_val} - {max_val} {unit}

Rules:
- Use simple language suitable for a general reader
- Address the patient as 'you/your'
- If the value is outside the supplied interval, list 2-3 possible explanations as possibilities, not conclusions
- Give one cautious next step
- Do not diagnose a disease or recommend starting/stopping medication or supplements
- Mention discussing the result with a qualified clinician
- Do not claim the supplied interval is universal; lab ranges vary by lab and patient context

Return ONLY this JSON object:
{{
  "explanation_en": "3-4 short sentences in simple English",
  "explanation_hi": "Same explanation in simple Hindi using Devanagari script",
  "possible_reasons": ["possible reason 1", "possible reason 2"],
  "action": "One practical next step"
}}"""

    fallback = {
        "explanation_en": (
            f"Your {name} result is {status.lower()}. Reference intervals depend on the lab "
            "and your circumstances. Please discuss this result with your doctor."
        ),
        "explanation_hi": (
            f"आपकी {name} की जाँच का परिणाम {status.lower()} है। सामान्य सीमा लैब और आपकी "
            "स्थिति के अनुसार अलग हो सकती है। कृपया अपने डॉक्टर से इस परिणाम पर चर्चा करें।"
        ),
        "possible_reasons": [],
        "action": "Discuss the result with a qualified clinician.",
    }
    try:
        raw = call_gemini(prompt, system, max_tokens=700)
        result = _parse_json_response(raw)
        if not isinstance(result, dict):
            raise ValueError("Expected a JSON object for the explanation.")
        return {**fallback, **result}
    except Exception as exc:
        print(f"Explanation failed for {name}: {exc}")
        return fallback


def generate_doctor_questions(abnormal_params: list) -> list:
    """Generate practical questions a patient may ask their clinician."""
    if not abnormal_params:
        return [
            "Could you review my report in the context of my symptoms and medical history?",
            "Do any results need to be repeated or monitored?",
            "When should I have my next check-up?",
        ]

    params_text = "\n".join(
        f"- {p.get('name', 'Unknown parameter')}: {p.get('value', 'N/A')} "
        f"{p.get('unit', '')} (Status: {p.get('status', 'Unknown')})"
        for p in abnormal_params
    )
    system = (
        "You help patients prepare for medical appointments. Return only a valid JSON array "
        "of strings. Do not diagnose or recommend a treatment."
    )
    prompt = f"""Generate 5-7 clear questions the patient can ask their clinician.

Results provided by the app:
{params_text}

Rules:
- Questions must relate to the results shown
- Use simple, practical language
- Include interpretation, possible follow-up, and whether repeat testing is appropriate
- Do not assume a disease or prescribe treatment

Return only a JSON array of question strings."""
    try:
        result = _parse_json_response(call_gemini(prompt, system, max_tokens=600))
        if isinstance(result, list):
            return [str(q) for q in result if isinstance(q, str)][:7]
        raise ValueError("Expected a JSON array.")
    except Exception as exc:
        print(f"Doctor-question generation failed: {exc}")
        return [
            "What do these results mean in the context of my health and symptoms?",
            "Could any of these results be affected by medicines, food, or recent activity?",
            "Do I need any follow-up or repeat tests?",
            "When should I schedule a follow-up appointment?",
            "Are there symptoms that should prompt me to seek medical care sooner?",
        ]


def generate_diet_suggestions(deficiencies: list) -> dict:
    """Generate general, cautious Indian-food suggestions for discussion with a clinician."""
    fallback = {
        "food_suggestions": [],
        "lifestyle_tips": [
            "Aim for a varied, balanced diet suited to your needs.",
            "Drink fluids regularly unless a clinician has advised you to restrict them.",
            "Ask a qualified clinician before starting supplements or making major diet changes.",
        ],
        "foods_to_avoid": [],
    }
    if not deficiencies:
        return fallback

    def_text = "\n".join(
        f"- {d.get('name', 'Unknown parameter')}: {d.get('status', 'Unknown')} "
        f"(Value: {d.get('value', 'N/A')} {d.get('unit', '')})"
        for d in deficiencies
    )
    system = (
        "You provide general nutrition education, not medical treatment. Return only valid JSON. "
        "Do not diagnose deficiencies from lab values alone or prescribe supplements."
    )
    prompt = f"""Offer general, affordable Indian food ideas that may support a balanced diet for the results listed.

Results:
{def_text}

Rules:
- Prefer common, affordable Indian foods and include vegetarian choices
- Do not claim food alone will correct a medical deficiency
- Do not recommend supplements, doses, restrictive diets, or stopping prescribed treatment
- Mention that the clinician should confirm whether a deficiency is present and advise treatment
- Avoid blanket foods-to-avoid advice unless clearly justified

Return ONLY this JSON object:
{{
  "food_suggestions": [
    {{"food": "food name", "reason": "general nutrition information", "frequency": "reasonable frequency", "how_to_eat": "simple serving idea"}}
  ],
  "lifestyle_tips": ["practical general tip"],
  "foods_to_avoid": []
}}"""
    try:
        result = _parse_json_response(call_gemini(prompt, system, max_tokens=900))
        if not isinstance(result, dict):
            raise ValueError("Expected a JSON object.")
        return {**fallback, **result}
    except Exception as exc:
        print(f"Diet-suggestion generation failed: {exc}")
        return fallback


def generate_health_summary(all_params: list, health_score: int) -> str:
    """Generate a cautious summary based on app-provided classifications."""
    normal_statuses = {"NORMAL", "WITHIN_RANGE"}
    borderline_statuses = {"BORDERLINE"}
    abnormal_statuses = {
        "ABNORMAL", "CRITICAL", "BELOW_RANGE", "ABOVE_RANGE", "LOW", "HIGH"
    }

    normal = [p for p in all_params if str(p.get("status", "")).upper() in normal_statuses]
    borderline = [p for p in all_params if str(p.get("status", "")).upper() in borderline_statuses]
    abnormal = [p for p in all_params if str(p.get("status", "")).upper() in abnormal_statuses]

    findings = ", ".join(str(p.get("name", "Unknown")) for p in abnormal) or "None flagged by the app"
    borderline_names = ", ".join(str(p.get("name", "Unknown")) for p in borderline) or "None flagged by the app"
    prompt = f"""Write a brief 3-4 sentence summary of these app classifications.

App-generated score (not a validated medical score): {health_score}/100
Within-range parameters: {len(normal)}
Borderline parameters: {len(borderline)}
Outside-range/flagged parameters: {len(abnormal)}
Flagged findings: {findings}
Borderline findings: {borderline_names}

Rules:
- Use simple, calm language
- Do not diagnose or imply that a numerical score measures overall health reliably
- State that reference ranges and results need clinical context
- Encourage the patient to discuss flagged results with a qualified clinician
- Keep under 100 words"""
    system = "You are NiraamayaAI, a cautious health-information assistant. Return plain text only."
    try:
        return call_gemini(prompt, system, max_tokens=250)
    except Exception as exc:
        print(f"Health-summary generation failed: {exc}")
        return (
            f"The app flagged {len(abnormal)} result(s) outside its configured reference ranges, "
            f"with {len(borderline)} borderline result(s) and {len(normal)} within-range result(s). "
            "These classifications are not a diagnosis, and the app score is not a validated medical score. "
            "Please review the report with a qualified clinician."
        )
