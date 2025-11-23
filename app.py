from flask import Flask, render_template, request, jsonify
import re
import json
import PyPDF2
from io import BytesIO
from PIL import Image
import os
import base64
import requests

# Cloud OCR using OCR.space API
def cloud_ocr(image_bytes):
    try:
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        url = 'https://api.ocr.space/parse/image'
        payload = {
            'base64Image': f'data:image/png;base64,{image_b64}',
            'apikey': 'helloworld',
            'language': 'eng'
        }
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()
        if result.get('IsErroredOnProcessing', True):
            return None
        return result['ParsedResults'][0]['ParsedText']
    except:
        return None

app = Flask(__name__)

class MedicalAnalyzer:
    def __init__(self):
        # Critical indicators that suggest immediate attention
        self.critical_keywords = [
            'malignant', 'cancer', 'tumor', 'metastasis', 'severe', 'critical',
            'emergency', 'acute', 'hemorrhage', 'stroke', 'heart attack'
        ]
        
        # Warning indicators
        self.warning_keywords = [
            'abnormal', 'elevated', 'high', 'low', 'irregular', 'inflammation',
            'infection', 'hypertension', 'diabetes', 'cholesterol'
        ]
        
        # Normal/positive indicators
        self.positive_keywords = [
            'normal', 'healthy', 'stable', 'good', 'excellent', 'within range',
            'no abnormalities', 'clear'
        ]

    def analyze_report(self, text):
        text_lower = text.lower()
        
        # Count keyword occurrences
        critical_count = sum(1 for keyword in self.critical_keywords if keyword in text_lower)
        warning_count = sum(1 for keyword in self.warning_keywords if keyword in text_lower)
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        
        # Determine overall status
        if critical_count > 0:
            status = "Critical"
            color = "#dc3545"
        elif warning_count > positive_count:
            status = "Needs Attention"
            color = "#ffc107"
        else:
            status = "Good"
            color = "#28a745"
        
        # Generate treatment plan
        treatment_plan = self._generate_treatment_plan(critical_count, warning_count, positive_count, text_lower)
        
        return {
            'status': status,
            'color': color,
            'critical_issues': critical_count,
            'warning_issues': warning_count,
            'positive_indicators': positive_count,
            'treatment_plan': treatment_plan
        }
    
    def _generate_treatment_plan(self, critical, warning, positive, text):
        treatment_plan = {
            'conditions': [],
            'medications': [],
            'lifestyle': [],
            'notes': []
        }
        
        if critical > 0:
            treatment_plan['conditions'].append("🚨 Critical Medical Condition: Severe abnormalities detected requiring immediate medical intervention and emergency care protocols.")
            treatment_plan['medications'].append("💊 URGENT: Immediate physician consultation required for emergency medication protocol")
            treatment_plan['lifestyle'].append("🚨 Strict bed rest until medical evaluation - avoid strenuous activities")
            treatment_plan['notes'].append("⚠️ Critical findings require immediate medical attention within 24 hours")
        
        if 'cholesterol' in text or 'lipid' in text:
            treatment_plan['conditions'].append("🫀 Dyslipidemia: Elevated cholesterol levels increasing cardiovascular disease risk. Requires lipid management and lifestyle modifications.")
            treatment_plan['medications'].append("💊 Statin therapy: Atorvastatin 20mg daily or Rosuvastatin 10mg daily (physician consultation required)")
            treatment_plan['lifestyle'].append("🥗 Mediterranean diet: <7% saturated fat, 25-35g fiber daily, omega-3 rich fish 2x/week")
            treatment_plan['notes'].append("📊 Target LDL <100mg/dL (or <70mg/dL if high cardiovascular risk)")
        
        if 'diabetes' in text or 'glucose' in text:
            treatment_plan['conditions'].append("🩺 Diabetes Mellitus: Chronic metabolic disorder characterized by elevated blood glucose levels. Requires comprehensive glucose management.")
            treatment_plan['medications'].append("💉 Metformin 500mg BID, consider GLP-1 agonists (Semaglutide) if HbA1c >7%")
            treatment_plan['lifestyle'].append("🍽️ Carbohydrate counting: 45-60g per meal, regular meal timing, avoid simple sugars")
            treatment_plan['notes'].append("🎯 Target HbA1c <7% for most adults, fasting glucose 80-130mg/dL")
        
        if 'blood pressure' in text or 'hypertension' in text:
            treatment_plan['conditions'].append("🫀 Hypertension: Elevated blood pressure increasing risk of cardiovascular disease, stroke, and kidney damage. Requires antihypertensive therapy.")
            treatment_plan['medications'].append("💊 ACE inhibitor (Lisinopril 10mg daily) or ARB (Losartan 50mg daily) - physician guided")
            treatment_plan['lifestyle'].append("🧂 DASH diet: <2300mg sodium daily, increase potassium (3500-5000mg), limit alcohol")
            treatment_plan['notes'].append("🎯 Target BP <130/80 mmHg, monitor daily at same time")
        
        if 'kidney' in text or 'renal' in text:
            treatment_plan['conditions'].append("🫘 Chronic Kidney Disease: Progressive loss of kidney function affecting waste filtration and electrolyte balance. Requires nephrology management.")
            treatment_plan['medications'].append("💊 Avoid NSAIDs, adjust medication doses based on eGFR, consider phosphate binders")
            treatment_plan['lifestyle'].append("💧 Fluid management: 1.5-2L daily unless restricted, low-protein diet (0.8g/kg body weight)")
            treatment_plan['notes'].append("🫘 Monitor creatinine, eGFR, and proteinuria every 3-6 months")
        
        if 'liver' in text or 'hepatic' in text:
            treatment_plan['conditions'].append("🦠 Hepatic Dysfunction: Impaired liver function affecting metabolism, detoxification, and protein synthesis. Requires hepatology evaluation.")
            treatment_plan['medications'].append("🚫 Discontinue hepatotoxic drugs (acetaminophen >3g/day, alcohol), consider ursodeoxycholic acid")
            treatment_plan['lifestyle'].append("🍾 Complete alcohol cessation, low-fat diet, avoid raw shellfish")
            treatment_plan['notes'].append("🦠 Monitor ALT, AST, bilirubin monthly until normalized")
        
        if warning > 0 and critical == 0:
            treatment_plan['medications'].append("💊 Continue current medications, discuss dose optimization with physician")
            treatment_plan['lifestyle'].append("📊 Daily symptom monitoring, maintain medication adherence >95%")
            treatment_plan['notes'].append("📅 Follow-up in 2-4 weeks for treatment response evaluation")
        
        if positive > warning:
            treatment_plan['medications'].append("✅ Maintain current therapeutic regimen - excellent medication response")
            treatment_plan['lifestyle'].append("🏃 Continue current exercise routine, maintain healthy dietary patterns")
            treatment_plan['notes'].append("🔄 Annual preventive care: lipid panel, HbA1c, comprehensive metabolic panel")
        
        return treatment_plan

analyzer = MedicalAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Handle file upload (PDF or Image)
        if 'report_file' in request.files:
            file = request.files['report_file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            filename = file.filename.lower()
            
            # Extract text based on file type
            if filename.endswith('.pdf'):
                # PDF processing
                pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
                report_text = ''
                for page in pdf_reader.pages:
                    report_text += page.extract_text() + '\n'
            
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                # Cloud OCR processing
                file_bytes = file.read()
                report_text = cloud_ocr(file_bytes)
                if not report_text:
                    return jsonify({'error': 'OCR processing failed. Please ensure image contains clear text.'}), 400
            
            else:
                return jsonify({'error': 'Unsupported file type. Please upload PDF or image files.'}), 400
        
        # Handle text input
        else:
            data = request.get_json()
            report_text = data.get('report_text', '')
        
        if not report_text.strip():
            return jsonify({'error': 'Please provide report text or upload a file'}), 400
        
        analysis = analyzer.analyze_report(report_text)
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)