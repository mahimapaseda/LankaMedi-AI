import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("demo_reports", exist_ok=True)

def generate_report(filename_base, title, hospital, patient_info, lab_data, notes):
    width, height = 1200, 1600
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 22)
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_header = font_sub = font_bold = font_normal = font_small = ImageFont.load_default()

    # Top Header banner
    draw.rectangle([(0, 0), (width, 140)], fill=(15, 76, 129))
    draw.text((60, 35), hospital, fill=(255, 255, 255), font=font_header)
    draw.text((60, 85), "Department of Clinical Pathology & Laboratory Medicine", fill=(200, 225, 245), font=font_sub)

    # Document Title
    draw.rectangle([(60, 165), (width - 60, 215)], fill=(240, 244, 248), outline=(210, 220, 230))
    draw.text((80, 175), title, fill=(20, 40, 60), font=font_bold)

    # Patient Metadata Box
    y_p = 235
    draw.rounded_rectangle([(60, y_p), (width - 60, y_p + 150)], radius=8, outline=(220, 225, 230), width=1)
    
    col1_x = 80
    col2_x = 650
    
    draw.text((col1_x, y_p + 20), f"Patient Name: {patient_info['name']}", fill=(40, 50, 60), font=font_bold)
    draw.text((col1_x, y_p + 60), f"NIC / Reg No: {patient_info['nic']}", fill=(60, 70, 80), font=font_normal)
    draw.text((col1_x, y_p + 100), f"Age / Gender: {patient_info['age_gender']}", fill=(60, 70, 80), font=font_normal)

    draw.text((col2_x, y_p + 20), f"Sample Date: {patient_info['date']}", fill=(60, 70, 80), font=font_normal)
    draw.text((col2_x, y_p + 60), f"Ref. Doctor: {patient_info['doctor']}", fill=(60, 70, 80), font=font_normal)
    draw.text((col2_x, y_p + 100), f"Status: {patient_info['status']}", fill=(0, 130, 80), font=font_bold)

    # Table Header
    y_t = y_p + 180
    draw.rectangle([(60, y_t), (width - 60, y_t + 45)], fill=(230, 238, 245))
    draw.text((80, y_t + 10), "TEST DESCRIPTION", fill=(30, 45, 60), font=font_bold)
    draw.text((550, y_t + 10), "RESULT", fill=(30, 45, 60), font=font_bold)
    draw.text((750, y_t + 10), "UNIT", fill=(30, 45, 60), font=font_bold)
    draw.text((920, y_t + 10), "REFERENCE RANGE", fill=(30, 45, 60), font=font_bold)

    # Table Rows
    curr_y = y_t + 55
    for row in lab_data:
        test, result, unit, ref, flag = row
        bg_col = (255, 243, 243) if flag == "HIGH" or flag == "CRITICAL" else (248, 252, 255)
        
        draw.rectangle([(60, curr_y - 5), (width - 60, curr_y + 35)], fill=bg_col)
        draw.text((80, curr_y), test, fill=(30, 40, 50), font=font_normal)
        
        # Colorize result
        res_color = (200, 20, 20) if flag in ["HIGH", "CRITICAL", "LOW"] else (20, 100, 40)
        draw.text((550, curr_y), str(result), fill=res_color, font=font_bold)
        draw.text((750, curr_y), unit, fill=(80, 90, 100), font=font_normal)
        draw.text((920, curr_y), ref, fill=(80, 90, 100), font=font_normal)

        if flag != "NORMAL":
            draw.text((670, curr_y), f"[{flag}]", fill=res_color, font=font_bold)

        curr_y += 45

    # Clinical Notes Box
    curr_y += 30
    draw.rounded_rectangle([(60, curr_y), (width - 60, curr_y + 160)], radius=8, outline=(230, 210, 160), fill=(255, 252, 240), width=1)
    draw.text((80, curr_y + 15), "LABORATORY REMARKS & CLINICAL NOTES:", fill=(140, 80, 10), font=font_bold)
    y_n = curr_y + 50
    for line in notes:
        draw.text((80, y_n), line, fill=(80, 60, 30), font=font_small)
        y_n += 26

    # Footer
    draw.line([(60, height - 90), (width - 60, height - 90)], fill=(200, 210, 220), width=1)
    draw.text((60, height - 70), "Verified by: Dr. N. Senanayake, MBBS, MD (Pathology) - Consultant Hematologist", fill=(100, 110, 120), font=font_small)
    draw.text((60, height - 45), "Confidential Medical Diagnostic Document - Protected under SL Medical Ordinance", fill=(130, 140, 150), font=font_small)

    png_path = f"demo_reports/{filename_base}.png"
    pdf_path = f"demo_reports/{filename_base}.pdf"
    img.save(png_path, "PNG")
    img.save(pdf_path, "PDF", resolution=150.0)
    print(f"Generated: {png_path} and {pdf_path}")

# 1. Durdans Renal Profile
generate_report(
    "demo_durdans_renal_failure_report",
    "RENAL FUNCTION TEST (RFT) & SERUM ELECTROLYTES",
    "DURDANS HOSPITAL PLC - COLOMBO 03",
    {
        "name": "K. M. Sunil Jayawardena",
        "nic": "196818204910",
        "age_gender": "56 Yrs / Male",
        "date": "04-Nov-2026 08:30 AM",
        "doctor": "Dr. Rohana Jayatillake",
        "status": "COMPLETED (CRITICAL ALERT)"
    },
    [
        ("Serum Creatinine", "2.8", "mg/dL", "0.7 - 1.3", "CRITICAL"),
        ("Blood Urea Nitrogen (BUN)", "78.4", "mg/dL", "7.0 - 20.0", "HIGH"),
        ("Estimated GFR (eGFR)", "24", "mL/min/1.73m2", "> 60.0", "CRITICAL"),
        ("Serum Potassium (K+)", "5.8", "mmol/L", "3.5 - 5.1", "HIGH"),
        ("Serum Sodium (Na+)", "136", "mmol/L", "135 - 145", "NORMAL"),
        ("Serum Uric Acid", "8.9", "mg/dL", "3.4 - 7.0", "HIGH")
    ],
    [
        "- Significant impairment of renal filtration (Stage 4 Severe Chronic Kidney Disease criteria).",
        "- Serum Potassium elevation (5.8 mmol/L) carries cardiac arrhythmia risk; urgent nephrology consult required.",
        "- Please correlate with 24-hour urine protein, renal ultrasound, and blood pressure profile.",
        "- Avoid NSAIDs, nephrotoxic agents, and high potassium dietary intake pending physician review."
    ]
)

# 2. Lanka Hospitals Normal Wellness Profile
generate_report(
    "demo_lankahospitals_normal_wellness_report",
    "EXECUTIVE HEALTH CHECKUP - COMPREHENSIVE BIOCHEMICAL PROFILE",
    "THE LANKA HOSPITALS PLC - ELVITIGALA MAWATHA, COLOMBO",
    {
        "name": "S. Dilani Gunasekera",
        "nic": "199274503210",
        "age_gender": "34 Yrs / Female",
        "date": "04-Nov-2026 09:15 AM",
        "doctor": "Dr. M. Perera",
        "status": "NORMAL / HEALTHY"
    },
    [
        ("Fasting Blood Sugar (FBS)", "88.0", "mg/dL", "70.0 - 100.0", "NORMAL"),
        ("Hemoglobin (Hb)", "13.4", "g/dL", "12.0 - 15.5", "NORMAL"),
        ("Total Platelet Count", "265,000", "/uL", "150,000 - 450,000", "NORMAL"),
        ("Serum Creatinine", "0.85", "mg/dL", "0.6 - 1.1", "NORMAL"),
        ("Total Cholesterol", "172", "mg/dL", "< 200.0", "NORMAL"),
        ("Serum ALT (SGPT)", "22.0", "U/L", "7.0 - 35.0", "NORMAL")
    ],
    [
        "- All evaluated hematological and metabolic parameters are within ideal physiological limits.",
        "- Glycemic control and renal clearance are optimal.",
        "- Continue standard physical activity (150 mins/week) and balanced dietary routine.",
        "- Recommended routine re-evaluation in 12 months."
    ]
)
