# LankaMedi AI

Smart Medical Report Analysis - A Sri Lankan AI-powered web application that analyzes medical reports and provides health status assessments with personalized recommendations for Sri Lankan healthcare.

## Features

- **🔬 AI Analysis**: Advanced text analysis for critical issues, warnings, and positive indicators
- **📊 Health Status**: Smart categorization as Good, Needs Attention, or Critical
- **💡 Smart Recommendations**: Personalized health insights based on report content
- **📱 Multi-Format Support**: Text input, PDF upload, and image OCR processing
- **🎨 Modern Interface**: Clean, responsive design with intuitive navigation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR** (optional, for image processing):
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`
   - **Note**: PDF and text input work without Tesseract

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Website**:
   Open http://localhost:5000 in your browser

## How It Works

1. Paste your medical report text into the textarea
2. Click "Analyze Report" 
3. Get instant AI analysis with:
   - Overall health status (Good/Warning/Critical)
   - Count of critical issues, warnings, and positive indicators
   - Personalized recommendations

## Medical Disclaimer

This AI analysis is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for medical decisions.