"""Clinical constants, Sri Lankan reference intervals, and national emergency contacts."""

STATUS_COLORS = {
    "Critical": "#dc3545",
    "Needs Attention": "#f59e0b",
    "Good": "#10b981",
}

# Sri Lankan Emergency Services & Helplines
SRI_LANKA_EMERGENCY_CONTACTS = {
    "ambulance": {
        "number": "1990",
        "name": "1990 Suwa Seriya Free Pre-Hospital Emergency Ambulance",
        "description": "Government of Sri Lanka national emergency response ambulance service.",
        "badge": "🚨 Call 1990 Immediately",
    },
    "poison_info": {
        "number": "011-2686143",
        "name": "National Poisons Information Centre (NHSL Colombo)",
        "description": "National Hospital of Sri Lanka emergency toxicology consultation.",
    },
    "mental_health": {
        "number": "1926",
        "name": "National Mental Health Helpline",
        "description": "NIMH Sri Lanka confidential mental health support.",
    },
    "police_emergency": {
        "number": "119",
        "name": "Police Emergency",
        "description": "Sri Lanka Police emergency operational room.",
    },
}

# Standard Clinical Reference Ranges in Sri Lanka (SLMA / MOH / College of Pathologists Guidelines)
CLINICAL_REFERENCE_RANGES = {
    "platelets": {
        "display_name": "Platelet Count (FBC)",
        "low": 150000,
        "high": 450000,
        "unit": "/uL",
        "critical_low": 50000,
        "severe_emergency_low": 20000,
        "category": "Hematology / Dengue Surveillance",
        "guidance": "Essential for Dengue hemorrhagic fever monitoring in Sri Lanka. Values below 100,000 warrant strict medical supervision. Values below 50,000/20,000 require immediate hospital admission.",
    },
    "hemoglobin": {
        "display_name": "Hemoglobin (Hb)",
        "low": 11.5,
        "high": 16.5,
        "unit": "g/dL",
        "critical_low": 7.0,
        "critical_high": 19.0,
        "category": "Hematology",
        "guidance": "Low hemoglobin indicates anemia. Severe drops require urgent hematological evaluation.",
    },
    "fbs": {
        "display_name": "Fasting Blood Sugar (FBS)",
        "low": 70.0,
        "high": 100.0,
        "unit": "mg/dL",
        "critical_low": 50.0,
        "critical_high": 300.0,
        "category": "Endocrinology / Diabetes",
        "guidance": "70-99 mg/dL is normal fasting. 100-125 mg/dL indicates impaired fasting glucose (prediabetes). >= 126 mg/dL indicates diabetes mellitus.",
    },
    "hba1c": {
        "display_name": "Glycated Hemoglobin (HbA1c)",
        "low": 4.0,
        "high": 5.7,
        "unit": "%",
        "critical_low": None,
        "critical_high": 10.0,
        "category": "Endocrinology / Diabetes",
        "guidance": "< 5.7% is normal. 5.7% - 6.4% indicates prediabetes. >= 6.5% indicates diabetes mellitus.",
    },
    "creatinine": {
        "display_name": "Serum Creatinine",
        "low": 0.6,
        "high": 1.2,
        "unit": "mg/dL",
        "critical_low": None,
        "critical_high": 3.0,
        "category": "Renal Function",
        "guidance": "Key renal marker. Elevated values suggest impaired glomerular filtration (CKD / AKI).",
    },
    "total_cholesterol": {
        "display_name": "Total Cholesterol",
        "low": 0.0,
        "high": 200.0,
        "unit": "mg/dL",
        "critical_low": None,
        "critical_high": 300.0,
        "category": "Lipid Profile",
        "guidance": "< 200 mg/dL is desirable. 200-239 mg/dL borderline high. >= 240 mg/dL is high.",
    },
    "ldl": {
        "display_name": "LDL Cholesterol",
        "low": 0.0,
        "high": 100.0,
        "unit": "mg/dL",
        "critical_low": None,
        "critical_high": 190.0,
        "category": "Lipid Profile",
        "guidance": "< 100 mg/dL optimal. >= 160 mg/dL high atherogenic risk.",
    },
    "hdl": {
        "display_name": "HDL Cholesterol",
        "low": 40.0,
        "high": 60.0,
        "unit": "mg/dL",
        "critical_low": 25.0,
        "critical_high": None,
        "category": "Lipid Profile",
        "guidance": "Cardioprotective cholesterol. Higher levels (> 50 mg/dL) are favorable.",
    },
    "triglycerides": {
        "display_name": "Serum Triglycerides",
        "low": 0.0,
        "high": 150.0,
        "unit": "mg/dL",
        "critical_low": None,
        "critical_high": 500.0,
        "category": "Lipid Profile",
        "guidance": "< 150 mg/dL normal. > 500 mg/dL severely high (pancreatitis risk).",
    },
    "sgpt_alt": {
        "display_name": "Alanine Aminotransferase (ALT / SGPT)",
        "low": 7.0,
        "high": 55.0,
        "unit": "U/L",
        "critical_low": None,
        "critical_high": 300.0,
        "category": "Liver Function",
        "guidance": "Hepatocellular enzyme. Marked elevation indicates acute liver injury or viral hepatitis.",
    },
    "sgot_ast": {
        "display_name": "Aspartate Aminotransferase (AST / SGOT)",
        "low": 8.0,
        "high": 48.0,
        "unit": "U/L",
        "critical_low": None,
        "critical_high": 300.0,
        "category": "Liver Function",
        "guidance": "Elevations seen in hepatic inflammation, skeletal muscle injury, or cardiac distress.",
    },
}

MEDICAL_DISCLAIMER_TEXT = (
    "LankaMedi AI is an assistive decision-support and educational tool designed for Sri Lankan healthcare context. "
    "It is NOT a replacement for qualified clinical diagnosis or licensed medical practitioner consultation. "
    "If you are experiencing severe symptoms or acute distress, contact emergency services (1990 in Sri Lanka) immediately."
)

