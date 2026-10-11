from __future__ import annotations

import os
import re
from typing import Any

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Run from the backend folder:
# python -m streamlit run app.py
load_dotenv()

st.set_page_config(
    page_title="NiraamayaAI | Lab Report Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    from services.pdf_extractor import extract_text
    from services.grok_service import (
        extract_parameters,
        generate_explanation,
        generate_doctor_questions,
        generate_diet_suggestions,
        generate_health_summary,
    )
    from services.reference_ranges import get_status
except ImportError as exc:
    st.error(
        "Could not import a NiraamayaAI service. Check that app.py is in the "
        "backend folder and the Python files are inside backend/services/."
    )
    st.code(str(exc))
    st.stop()


st.markdown(
    """
    <style>
      .main-title {font-size: 2.2rem; font-weight: 750; margin-bottom: 0.1rem;}
      .sub-title {color: #6b7280; margin-top: 0;}
      .small-note {font-size: 0.88rem; color: #6b7280;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🩺 NiraamayaAI</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">A multilingual lab-report interpretation demo</p>',
    unsafe_allow_html=True,
)
st.info(
    "Educational prototype only. It does not diagnose medical conditions or replace a clinician. "
    "Use a synthetic or consented, de-identified report for demonstrations."
)

api_key_present = bool(os.getenv("GEMINI_API_KEY"))

with st.sidebar:
    st.header("Report settings")
    gender_label = st.selectbox(
        "Reference-range profile",
        options=["Not specified", "Male", "Female"],
        index=0,
        help=(
            "General ranges vary by laboratory, age, and other factors. "
            "Prefer the interval printed on the report."
        ),
    )
    gender = {
        "Not specified": "default",
        "Male": "male",
        "Female": "female",
    }[gender_label]

    st.caption("API provider: Google Gemini")
    if not api_key_present:
        st.error(
            "GEMINI_API_KEY not detected. Add it to backend/.env and restart Streamlit."
        )
    else:
        st.success("Gemini API key detected.")

    st.divider()
    st.caption(
        "Prototype workflow: upload PDF → extract values → compare ranges → generate explanations."
    )

uploaded_file = st.file_uploader(
    "Upload a laboratory report (PDF)",
    type=["pdf"],
)


def legacy_status(status: str) -> str:
    """Map range-check statuses to labels expected by the existing summary service."""
    return {
        "WITHIN_RANGE": "NORMAL",
        "BELOW_RANGE": "ABNORMAL",
        "ABOVE_RANGE": "ABNORMAL",
        "UNKNOWN": "UNKNOWN",
    }.get(status, "UNKNOWN")


def normalize_extracted_parameter(
    param: dict[str, Any], selected_gender: str
) -> dict[str, Any]:
    """Validate an extracted value and compare it with the report or configured range."""
    name = str(param.get("name", "Unknown parameter"))
    key = str(param.get("key") or name).strip().lower()
    value = param.get("value")
    unit = str(param.get("unit") or "")

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return {
            **param,
            "name": name,
            "key": key,
            "value": value,
            "unit": unit,
            "status": "UNKNOWN",
            "direction": "UNKNOWN",
            "display_status": "Could not compare",
            "range_text": str(param.get("reference_range") or "Not available"),
            "min_val": None,
            "max_val": None,
            "note": "The extracted value was not numeric, so it was not compared.",
        }

    checked = get_status(key, numeric_value, selected_gender)
    status = checked.get("status", "UNKNOWN")
    direction = checked.get("direction", "UNKNOWN")

    # Prefer a numeric reference interval printed in the report.
    report_range = str(param.get("reference_range") or "").strip()
    range_text = report_range or (
        f"{checked['min']:g}–{checked['max']:g} {checked.get('unit', unit)}"
        if checked.get("min") is not None and checked.get("max") is not None
        else "Not available"
    )

    if report_range:
        match = re.search(
            r"(-?\d+(?:\.\d+)?)\s*(?:-|–|to)\s*(-?\d+(?:\.\d+)?)",
            report_range,
            re.IGNORECASE,
        )
        if match:
            report_min, report_max = float(match.group(1)), float(match.group(2))
            if report_min <= report_max:
                if numeric_value < report_min:
                    status, direction = "BELOW_RANGE", "LOW"
                elif numeric_value > report_max:
                    status, direction = "ABOVE_RANGE", "HIGH"
                else:
                    status, direction = "WITHIN_RANGE", "NORMAL"
                checked["min"], checked["max"] = report_min, report_max

    return {
        **param,
        "name": name,
        "key": checked.get("key", key),
        "value": numeric_value,
        "unit": unit or checked.get("unit", ""),
        "status": status,
        "direction": direction,
        "display_status": {
            "WITHIN_RANGE": "Within range",
            "BELOW_RANGE": "Below range",
            "ABOVE_RANGE": "Above range",
            "UNKNOWN": "Range unavailable",
        }.get(status, status),
        "range_text": range_text,
        "min_val": checked.get("min"),
        "max_val": checked.get("max"),
        "note": checked.get(
            "note",
            "Use the laboratory's own reference interval when available.",
        ),
    }


if uploaded_file is not None:
    st.write(
        f"**Selected file:** {uploaded_file.name} · {uploaded_file.size / 1024:.1f} KB"
    )

    if st.button("Analyze lab report", type="primary", use_container_width=True):
        # Check the Gemini key because this app now uses Gemini, not Grok.
        if not os.getenv("GEMINI_API_KEY"):
            st.error(
                "GEMINI_API_KEY is missing. Add it to backend/.env and restart Streamlit."
            )
        else:
            with st.spinner("Extracting text from the PDF…"):
                pdf_bytes = uploaded_file.getvalue()
                extracted_text = extract_text(pdf_bytes)

            if not extracted_text or len(extracted_text.strip()) < 10:
                st.error(
                    "No readable text was extracted. This PDF may be scanned or image-only. "
                    "This demo currently needs a text-based PDF; OCR is not included."
                )
            else:
                with st.expander("Preview extracted PDF text"):
                    st.text(extracted_text[:12000])

                with st.spinner("Extracting laboratory parameters with Gemini…"):
                    raw_params = extract_parameters(extracted_text)

                if not raw_params:
                    st.error(
                        "No lab parameters were returned. Check the PDF text and Gemini model/API configuration."
                    )
                else:
                    normalized = [
                        normalize_extracted_parameter(p, gender)
                        for p in raw_params
                        if isinstance(p, dict)
                    ]
                    st.session_state["niraamaya_params"] = normalized
                    st.session_state["niraamaya_filename"] = uploaded_file.name
                    st.session_state["niraamaya_text"] = extracted_text
                    st.session_state.pop("niraamaya_summary", None)
                    st.session_state.pop("niraamaya_questions", None)
                    st.session_state.pop("niraamaya_diet", None)
                    st.success(
                        f"Extracted {len(normalized)} parameter(s). Review the results below."
                    )


if st.session_state.get("niraamaya_params"):
    params = st.session_state["niraamaya_params"]
    st.divider()
    st.subheader("Report overview")

    total = len(params)
    within = sum(p.get("status") == "WITHIN_RANGE" for p in params)
    outside = sum(
        p.get("status") in {"BELOW_RANGE", "ABOVE_RANGE"} for p in params
    )
    unknown = sum(p.get("status") == "UNKNOWN" for p in params)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Parameters extracted", total)
    c2.metric("Within configured range", within)
    c3.metric("Outside configured range", outside)
    c4.metric("Range unavailable", unknown)

    st.subheader("Extracted results")
    table_rows = [
        {
            "Parameter": p.get("name", "Unknown"),
            "Value": p.get("value", "—"),
            "Unit": p.get("unit", ""),
            "Reference interval": p.get("range_text", "Not available"),
            "Comparison": p.get("display_status", "Unknown"),
        }
        for p in params
    ]
    st.dataframe(
        pd.DataFrame(table_rows),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(
        "Range comparisons are approximate. A result outside a reference interval does not automatically mean disease, "
        "and a result inside it does not guarantee good health."
    )

    st.subheader("Explain a parameter")
    selectable = [
        p
        for p in params
        if p.get("status") != "UNKNOWN"
        and p.get("min_val") is not None
        and p.get("max_val") is not None
    ]

    if selectable:
        labels = [
            f"{p['name']} — {p['value']} {p.get('unit', '')} ({p['display_status']})"
            for p in selectable
        ]
        chosen_label = st.selectbox("Choose a parameter", options=labels)
        chosen = selectable[labels.index(chosen_label)]

        if st.button("Generate English + Hindi explanation"):
            with st.spinner("Generating explanation with Gemini…"):
                explanation = generate_explanation(
                    name=chosen.get("name", "parameter"),
                    value=float(chosen["value"]),
                    unit=chosen.get("unit", ""),
                    status=chosen.get(
                        "direction", chosen.get("status", "UNKNOWN")
                    ),
                    min_val=float(chosen["min_val"]),
                    max_val=float(chosen["max_val"]),
                )

            st.markdown("**English**")
            st.write(explanation.get("explanation_en", "No explanation returned."))
            st.markdown("**हिंदी**")
            st.write(explanation.get("explanation_hi", "व्याख्या उपलब्ध नहीं है।"))

            reasons = explanation.get("possible_reasons", [])
            if reasons:
                st.markdown("**Possible reasons to discuss with a clinician**")
                for reason in reasons:
                    st.markdown(f"- {reason}")

            if explanation.get("action"):
                st.markdown("**Suggested next step**")
                st.write(explanation["action"])
    else:
        st.info(
            "No parameter with a recognized configured interval is available for this explanation demo."
        )

    st.divider()
    st.subheader("AI-generated report summary")
    if st.button("Generate overall summary", use_container_width=True):
        legacy_params = [
            {**p, "status": legacy_status(p.get("status", "UNKNOWN"))}
            for p in params
        ]
        # Placeholder only; this is not a validated clinical health score.
        placeholder_score = 0
        with st.spinner("Generating summary with Gemini…"):
            st.session_state["niraamaya_summary"] = generate_health_summary(
                legacy_params, placeholder_score
            )

    if st.session_state.get("niraamaya_summary"):
        st.write(st.session_state["niraamaya_summary"])
        st.caption(
            "The score field used internally is a placeholder, not a validated health score."
        )

    abnormal_params = [
        {**p, "status": legacy_status(p.get("status", "UNKNOWN"))}
        for p in params
        if p.get("status") in {"BELOW_RANGE", "ABOVE_RANGE"}
    ]

    st.subheader("Questions to discuss with your doctor")
    if st.button("Generate doctor questions", use_container_width=True):
        with st.spinner("Preparing questions with Gemini…"):
            st.session_state["niraamaya_questions"] = generate_doctor_questions(
                abnormal_params
            )

    if st.session_state.get("niraamaya_questions"):
        for i, question in enumerate(
            st.session_state["niraamaya_questions"], start=1
        ):
            st.markdown(f"{i}. {question}")

    st.subheader("General food and lifestyle ideas")
    if abnormal_params:
        if st.button("Generate general diet suggestions", use_container_width=True):
            with st.spinner("Generating general suggestions with Gemini…"):
                st.session_state["niraamaya_diet"] = generate_diet_suggestions(
                    abnormal_params
                )

        diet = st.session_state.get("niraamaya_diet")
        if diet:
            food_suggestions = diet.get("food_suggestions", [])
            if food_suggestions:
                st.markdown("**Food suggestions**")
                for item in food_suggestions:
                    if isinstance(item, dict):
                        st.markdown(
                            f"- **{item.get('food', 'Food')}** — {item.get('reason', '')} "
                            f"*({item.get('frequency', 'As appropriate')})*"
                        )
                        if item.get("how_to_eat"):
                            st.caption(item["how_to_eat"])

            for section, title in [
                ("lifestyle_tips", "Lifestyle tips"),
                ("foods_to_avoid", "Things to discuss/consider"),
            ]:
                items = diet.get(section, [])
                if items:
                    st.markdown(f"**{title}**")
                    for item in items:
                        st.markdown(f"- {item}")

            st.caption(
                "Diet suggestions are general information, not treatment. "
                "Discuss deficiencies and supplements with a clinician."
            )
    else:
        st.info(
            "No out-of-range values were identified by the configured comparison, "
            "so diet suggestions are not generated."
        )

    with st.expander("Technical notes and limitations"):
        st.markdown(
            "- PDF extraction currently supports text-based PDFs; scanned PDFs need OCR, which is not included.\n"
            "- AI extraction can miss, misread, or invent values. Verify every result against the original report.\n"
            "- Generic reference ranges are only a fallback; the lab's own interval should take priority.\n"
            "- The app does not calculate a clinically validated health score and does not provide diagnosis or triage."
        )

st.divider()
st.markdown(
    '<p class="small-note">NiraamayaAI prototype · For demonstration and educational use only.</p>',
    unsafe_allow_html=True,
)
