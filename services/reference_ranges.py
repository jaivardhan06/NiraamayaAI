"""
Reference ranges for the NiraamayaAI demonstration.

IMPORTANT:
- These are general reference values carried over from the project's
  original reference-range file. Actual ranges vary by laboratory,
  assay, age, sex, pregnancy status, and other clinical factors.
- Prefer the reference interval printed on the uploaded report when
  it is available and readable.
- This module flags only whether a value is below, within, or above
  the selected interval. It does not diagnose disease or determine
  clinical urgency.
"""

REFERENCE_RANGES = {
    "hemoglobin": {
        "display_name": "Hemoglobin",
        "unit": "g/dL",
        "male": {"min": 13.0, "max": 17.0},
        "female": {"min": 12.0, "max": 15.0},
        "default": {"min": 12.0, "max": 17.0},
        "category": "Blood",
        "aliases": ["hb", "haemoglobin", "hgb"],
    },
    "rbc": {
        "display_name": "RBC Count",
        "unit": "million/µL",
        "male": {"min": 4.5, "max": 5.9},
        "female": {"min": 4.0, "max": 5.2},
        "default": {"min": 4.0, "max": 5.9},
        "category": "Blood",
        "aliases": ["rbc count", "red blood cell count", "red blood cells"],
    },
    "wbc": {
        "display_name": "WBC Count",
        "unit": "thousand/µL",
        "default": {"min": 4.0, "max": 11.0},
        "category": "Blood",
        "aliases": ["wbc count", "white blood cell count", "total leukocyte count", "tlc"],
    },
    "platelets": {
        "display_name": "Platelets",
        "unit": "thousand/µL",
        "default": {"min": 150.0, "max": 400.0},
        "category": "Blood",
        "aliases": ["platelet count", "platelets count", "plt"],
    },
    "hematocrit": {
        "display_name": "Hematocrit (PCV)",
        "unit": "%",
        "male": {"min": 40.0, "max": 52.0},
        "female": {"min": 36.0, "max": 48.0},
        "default": {"min": 36.0, "max": 52.0},
        "category": "Blood",
        "aliases": ["hematocrit", "pcv", "packed cell volume", "hct"],
    },
    "mcv": {
        "display_name": "MCV",
        "unit": "fL",
        "default": {"min": 80.0, "max": 100.0},
        "category": "Blood",
        "aliases": ["mean corpuscular volume"],
    },
    "mch": {
        "display_name": "MCH",
        "unit": "pg",
        "default": {"min": 27.0, "max": 33.0},
        "category": "Blood",
        "aliases": ["mean corpuscular hemoglobin", "mean corpuscular haemoglobin"],
    },
    "mchc": {
        "display_name": "MCHC",
        "unit": "g/dL",
        "default": {"min": 32.0, "max": 36.0},
        "category": "Blood",
        "aliases": ["mean corpuscular hemoglobin concentration", "mean corpuscular haemoglobin concentration"],
    },
    "glucose_fasting": {
        "display_name": "Glucose (Fasting)",
        "unit": "mg/dL",
        "default": {"min": 70.0, "max": 100.0},
        "category": "Metabolic",
        "aliases": ["fasting glucose", "fasting blood sugar", "fbs", "fasting plasma glucose", "fpg"],
    },
    "glucose_pp": {
        "display_name": "Glucose (Post Prandial)",
        "unit": "mg/dL",
        "default": {"min": 70.0, "max": 140.0},
        "category": "Metabolic",
        "aliases": ["post prandial glucose", "postprandial glucose", "pp glucose", "ppbs", "2 hour glucose"],
    },
    "glucose_random": {
        "display_name": "Glucose (Random)",
        "unit": "mg/dL",
        "default": {"min": 70.0, "max": 140.0},
        "category": "Metabolic",
        "aliases": ["random glucose", "random blood sugar", "rbs", "random blood glucose"],
    },
    "hba1c": {
        "display_name": "HbA1c",
        "unit": "%",
        "default": {"min": 4.0, "max": 5.7},
        "category": "Metabolic",
        "aliases": ["haemoglobin a1c", "hemoglobin a1c", "glycated hemoglobin", "glycosylated hemoglobin"],
    },
    "tsh": {
        "display_name": "TSH",
        "unit": "µIU/mL",
        "default": {"min": 0.4, "max": 4.0},
        "category": "Thyroid",
        "aliases": ["thyroid stimulating hormone", "thyrotropin"],
    },
    "t3": {
        "display_name": "T3 (Triiodothyronine)",
        "unit": "ng/dL",
        "default": {"min": 80.0, "max": 200.0},
        "category": "Thyroid",
        "aliases": ["triiodothyronine", "total t3"],
    },
    "t4": {
        "display_name": "T4 (Thyroxine)",
        "unit": "µg/dL",
        "default": {"min": 5.0, "max": 12.0},
        "category": "Thyroid",
        "aliases": ["thyroxine", "total t4"],
    },
    "ferritin": {
        "display_name": "Ferritin",
        "unit": "ng/mL",
        "male": {"min": 24.0, "max": 336.0},
        "female": {"min": 11.0, "max": 307.0},
        "default": {"min": 11.0, "max": 336.0},
        "category": "Iron",
        "aliases": ["serum ferritin"],
    },
    "serum_iron": {
        "display_name": "Serum Iron",
        "unit": "µg/dL",
        "male": {"min": 65.0, "max": 175.0},
        "female": {"min": 50.0, "max": 170.0},
        "default": {"min": 50.0, "max": 175.0},
        "category": "Iron",
        "aliases": ["iron serum", "serum fe"],
    },
    "tibc": {
        "display_name": "TIBC",
        "unit": "µg/dL",
        "default": {"min": 250.0, "max": 370.0},
        "category": "Iron",
        "aliases": ["total iron binding capacity"],
    },
    "vitamin_d": {
        "display_name": "Vitamin D (25-OH)",
        "unit": "ng/mL",
        "default": {"min": 30.0, "max": 100.0},
        "category": "Vitamins",
        "aliases": ["25-oh vitamin d", "25 hydroxy vitamin d", "25(oh)d", "vitamin d total"],
    },
    "vitamin_b12": {
        "display_name": "Vitamin B12",
        "unit": "pg/mL",
        "default": {"min": 200.0, "max": 900.0},
        "category": "Vitamins",
        "aliases": ["b12", "cobalamin", "serum b12"],
    },
    "folate": {
        "display_name": "Folate (Folic Acid)",
        "unit": "ng/mL",
        "default": {"min": 3.0, "max": 17.0},
        "category": "Vitamins",
        "aliases": ["folic acid", "serum folate"],
    },
    "creatinine": {
        "display_name": "Creatinine",
        "unit": "mg/dL",
        "male": {"min": 0.7, "max": 1.3},
        "female": {"min": 0.5, "max": 1.1},
        "default": {"min": 0.5, "max": 1.3},
        "category": "Kidney",
        "aliases": ["serum creatinine"],
    },
    "urea": {
        "display_name": "Blood Urea",
        "unit": "mg/dL",
        "default": {"min": 15.0, "max": 45.0},
        "category": "Kidney",
        "aliases": ["serum urea"],
    },
    "bun": {
        "display_name": "BUN (Blood Urea Nitrogen)",
        "unit": "mg/dL",
        "default": {"min": 7.0, "max": 20.0},
        "category": "Kidney",
        "aliases": ["blood urea nitrogen"],
    },
    "uric_acid": {
        "display_name": "Uric Acid",
        "unit": "mg/dL",
        "male": {"min": 3.5, "max": 7.2},
        "female": {"min": 2.6, "max": 6.0},
        "default": {"min": 2.6, "max": 7.2},
        "category": "Kidney",
        "aliases": ["serum uric acid"],
    },
    "alt": {
        "display_name": "ALT (SGPT)",
        "unit": "U/L",
        "default": {"min": 7.0, "max": 56.0},
        "category": "Liver",
        "aliases": ["sgpt", "alanine aminotransferase", "alanine transaminase"],
    },
    "ast": {
        "display_name": "AST (SGOT)",
        "unit": "U/L",
        "default": {"min": 10.0, "max": 40.0},
        "category": "Liver",
        "aliases": ["sgot", "aspartate aminotransferase", "aspartate transaminase"],
    },
    "alp": {
        "display_name": "ALP (Alkaline Phosphatase)",
        "unit": "U/L",
        "default": {"min": 44.0, "max": 147.0},
        "category": "Liver",
        "aliases": ["alkaline phosphatase"],
    },
    "bilirubin_total": {
        "display_name": "Bilirubin (Total)",
        "unit": "mg/dL",
        "default": {"min": 0.1, "max": 1.2},
        "category": "Liver",
        "aliases": ["total bilirubin", "serum bilirubin total"],
    },
    "bilirubin_direct": {
        "display_name": "Bilirubin (Direct)",
        "unit": "mg/dL",
        "default": {"min": 0.0, "max": 0.3},
        "category": "Liver",
        "aliases": ["direct bilirubin", "conjugated bilirubin"],
    },
    "total_protein": {
        "display_name": "Total Protein",
        "unit": "g/dL",
        "default": {"min": 6.0, "max": 8.3},
        "category": "Liver",
        "aliases": ["serum total protein"],
    },
    "albumin": {
        "display_name": "Albumin",
        "unit": "g/dL",
        "default": {"min": 3.5, "max": 5.0},
        "category": "Liver",
        "aliases": ["serum albumin"],
    },
    "total_cholesterol": {
        "display_name": "Total Cholesterol",
        "unit": "mg/dL",
        "default": {"min": 0.0, "max": 200.0},
        "category": "Lipid",
        "aliases": ["cholesterol total", "serum cholesterol"],
    },
    "hdl": {
        "display_name": "HDL Cholesterol",
        "unit": "mg/dL",
        "male": {"min": 40.0, "max": 60.0},
        "female": {"min": 50.0, "max": 60.0},
        "default": {"min": 40.0, "max": 60.0},
        "category": "Lipid",
        "aliases": ["hdl-c", "hdl cholesterol"],
    },
    "ldl": {
        "display_name": "LDL Cholesterol",
        "unit": "mg/dL",
        "default": {"min": 0.0, "max": 100.0},
        "category": "Lipid",
        "aliases": ["ldl-c", "ldl cholesterol"],
    },
    "triglycerides": {
        "display_name": "Triglycerides",
        "unit": "mg/dL",
        "default": {"min": 0.0, "max": 150.0},
        "category": "Lipid",
        "aliases": ["triglyceride", "serum triglycerides", "tg"],
    },
    "vldl": {
        "display_name": "VLDL Cholesterol",
        "unit": "mg/dL",
        "default": {"min": 0.0, "max": 30.0},
        "category": "Lipid",
        "aliases": ["vldl-c", "vldl cholesterol"],
    },
    "sodium": {
        "display_name": "Sodium",
        "unit": "mEq/L",
        "default": {"min": 136.0, "max": 145.0},
        "category": "Electrolytes",
        "aliases": ["serum sodium", "na"],
    },
    "potassium": {
        "display_name": "Potassium",
        "unit": "mEq/L",
        "default": {"min": 3.5, "max": 5.1},
        "category": "Electrolytes",
        "aliases": ["serum potassium", "k"],
    },
    "calcium": {
        "display_name": "Calcium",
        "unit": "mg/dL",
        "default": {"min": 8.5, "max": 10.5},
        "category": "Electrolytes",
        "aliases": ["serum calcium", "total calcium"],
    },
    "magnesium": {
        "display_name": "Magnesium",
        "unit": "mg/dL",
        "default": {"min": 1.7, "max": 2.2},
        "category": "Electrolytes",
        "aliases": ["serum magnesium"],
    },
}


def _normalize_key(text: str) -> str:
    """Normalize a test name for exact/alias matching."""
    return " ".join(
        text.lower()
        .replace("_", " ")
        .replace("-", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("/", " ")
        .split()
    )


def find_parameter(key: str):
    """
    Find a parameter using an exact canonical key, display name, or alias.
    Returns (canonical_key, parameter_dict), or (None, None).
    Avoids broad substring matching that can confuse related tests.
    """
    if not isinstance(key, str) or not key.strip():
        return None, None

    normalized = _normalize_key(key)

    # Exact canonical-key match
    for canonical_key, param in REFERENCE_RANGES.items():
        if normalized == _normalize_key(canonical_key):
            return canonical_key, param

    # Exact display-name or alias match
    for canonical_key, param in REFERENCE_RANGES.items():
        candidates = [param["display_name"], *param.get("aliases", [])]
        if any(normalized == _normalize_key(candidate) for candidate in candidates):
            return canonical_key, param

    return None, None


def get_status(key: str, value: float, gender: str = "default") -> dict:
    """
    Compare a numeric value with the configured interval.

    Returns a dictionary with status BELOW_RANGE, WITHIN_RANGE,
    ABOVE_RANGE, or UNKNOWN. This is a range comparison only; it does
    not assess clinical urgency or diagnose a condition.

    `gender` accepts "male", "female", or "default".
    """
    canonical_key, param = find_parameter(key)

    if not param:
        return {"status": "UNKNOWN", "message": "Parameter not recognized."}

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return {
            "status": "UNKNOWN",
            "display_name": param["display_name"],
            "message": "Value is not numeric.",
        }

    # Avoid accepting NaN and infinity as laboratory values.
    if numeric_value != numeric_value or numeric_value in (float("inf"), float("-inf")):
        return {
            "status": "UNKNOWN",
            "display_name": param["display_name"],
            "message": "Value is not a finite number.",
        }

    selected_gender = (gender or "default").strip().lower()
    if selected_gender not in {"male", "female", "default"}:
        selected_gender = "default"

    ref = param.get(selected_gender) or param.get("default")
    if not ref:
        return {
            "status": "UNKNOWN",
            "display_name": param["display_name"],
            "message": "No reference interval is configured.",
        }

    min_val = float(ref["min"])
    max_val = float(ref["max"])

    if numeric_value < min_val:
        status = "BELOW_RANGE"
        direction = "LOW"
    elif numeric_value > max_val:
        status = "ABOVE_RANGE"
        direction = "HIGH"
    else:
        status = "WITHIN_RANGE"
        direction = "NORMAL"

    return {
        "key": canonical_key,
        "status": status,
        "direction": direction,
        "value": numeric_value,
        "min": min_val,
        "max": max_val,
        "unit": param["unit"],
        "category": param["category"],
        "display_name": param["display_name"],
        "message": {
            "BELOW_RANGE": "Below the configured reference interval.",
            "WITHIN_RANGE": "Within the configured reference interval.",
            "ABOVE_RANGE": "Above the configured reference interval.",
        }[status],
        "note": (
            "Use the interval printed on the report when available. "
            "This comparison alone is not a diagnosis or an assessment "
            "of clinical urgency."
        ),
    }
