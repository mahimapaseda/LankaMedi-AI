# 🏥 LankaMedi AI — AI Medical Report Analysis Platform (v2.0)

**Smart Medical Decision-Support & Diagnostic Report Analysis for Sri Lanka** 🇱🇰

[![AI Medical Analysis](https://img.shields.io/badge/AI-Medical%20Analysis-blue)](https://github.com/mahimapaseda/LankaMedi-AI)
[![Sri Lanka Healthcare](https://img.shields.io/badge/Healthcare-Sri%20Lanka-green)](https://github.com/mahimapaseda/LankaMedi-AI)
[![Architecture v2.0](https://img.shields.io/badge/Architecture-Clean%20Modular%20v2.0-blueviolet)](https://github.com/mahimapaseda/LankaMedi-AI)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LankaMedi AI is a cutting-edge clinical decision-support and medical report analysis platform re-architected specifically for the **Sri Lankan healthcare ecosystem**. The system combines multi-provider AI reasoning, rule-based biomarker reference range evaluation, patient privacy de-identification, and national emergency triage protocols.

---

## ✨ Features & Capabilities (v2.0 Redesign)

- **🔬 Hybrid Biomarker Range Engine**: Automatically evaluates diagnostic lab parameters (Platelets, Fasting Blood Sugar, HbA1c, Serum Creatinine, Lipid Profile, LFTs) against Sri Lankan reference intervals (SLMA/MOH guidelines) with real-time visual status cards.
- **🚨 1990 Suwa Seriya Emergency Triage**: Detects critical life-threatening conditions (e.g. Dengue thrombocytopenia with Platelets < 50,000 /uL, severe acute diabetic derangement, critical anemia) and triggers immediate emergency alert banners with one-click direct dialing to **1990**.
- **🌐 Trilingual Localization**: Full native language support for **English**, **Sinhala (සිංහල)**, and **Tamil (தமிழ்)**.
- **🛡️ Patient Privacy & PII/PHI De-identification**: Compliant with data protection principles. Automatically masks Sri Lankan National Identity Card (NIC) numbers, telephone numbers, emails, and patient names before sending data to AI providers.
- **🤖 Multi-Provider LLM Orchestration**: Automated cascading fallback across **NVIDIA NIM** (`nvidia/nemotron-3.5-bolt-e4b`), **Google Gemini**, and **OpenAI/Groq/Ollama**.
- **📄 Dual-Pipeline Ingestion**: Supports electronic PDFs (`pypdf`), digitized documents, and high-resolution medical images with automated pre-processing and OCR.
- **🖨️ Clinical Summary Export**: One-click print and PDF generation for patients and attending physicians.

---

## 🏗️ System Architecture

```text
LankaMedi-AI/
├── core/                        # Typed configuration, Sri Lankan clinical constants & security
│   ├── config.py                # Environment and provider settings
│   ├── constants.py             # Sri Lankan lab reference ranges & emergency hotlines
│   └── security.py              # PII scrubber (NIC, Phone, Name redaction) & file validators
│
├── services/                    # Business logic and external orchestrations
│   ├── biomarker_service.py     # Rule-based lab parameter evaluator & emergency triage
│   ├── document_service.py      # PDF text extractor & image pre-processor
│   ├── ocr_service.py           # Optical Character Recognition pipeline
│   └── llm_service.py           # Multi-provider LLM orchestrator (NVIDIA, Gemini, OpenAI)
│
├── schemas/                     # Strongly-typed Pydantic validation models
│   └── analysis_schema.py       # BiomarkerResult, TreatmentPlan, EmergencyAlert, AnalysisResponse
│
├── routes/                      # Modular Flask blueprints
│   ├── api.py                   # REST API (/api/v1/analyze, /api/v1/health, /api/v1/reference-ranges)
│   └── web.py                   # Web interface router
│
├── static/                      # Modular frontend assets
│   ├── css/main.css             # Glassmorphism, mobile-first design, print styles
│   └── js/
│       ├── i18n.js              # Trilingual translation engine (EN, SI, TA)
│       └── app.js               # Dropzone, preview, counter animations & API client
│
├── templates/
│   └── index.html               # Semantic, accessible UI with 1990 emergency banner
│
├── app.py                       # Application factory (create_app)
└── wsgi.py                      # Production WSGI entry point
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/mahimapaseda/LankaMedi-AI.git
cd LankaMedi-AI
```

### 2. Set up virtual environment & install dependencies
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and configure your API keys:
```ini
# Primary LLM: NVIDIA NIM
NVIDIA_API_KEY=nvapi-your-key-here
NVIDIA_MODEL=nvidia/nemotron-3.5-bolt-e4b

# Fallback LLMs (Optional)
GEMINI_API_KEY=
OPENAI_API_KEY=

# Cloud OCR (Optional, defaults to public tier if empty)
OCR_SPACE_API_KEY=
```

### 4. Run development server
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/analyze` | Ingests multipart file (`report_file`) or JSON (`report_text`), returns clinical assessment. |
| `POST` | `/analyze` | Legacy alias for backward compatibility. |
| `GET` | `/api/v1/health` | System health check and active AI model providers. |
| `GET` | `/api/v1/reference-ranges` | Established Sri Lankan clinical reference intervals and emergency contacts. |
| `POST` | `/api/v1/deidentify` | Previews patient PII redaction without running full analysis. |

---

## ⚠️ Medical AI Disclaimer & Compliance

**IMPORTANT MEDICAL NOTICE**: LankaMedi AI is an **artificial intelligence clinical decision-support and educational tool**. It is designed for informational and educational purposes only.

- **Does NOT replace professional medical diagnosis** or clinical judgment.
- **Should NOT be used for emergency medical situations** — In Sri Lanka, dial **1990 Suwa Seriya** immediately.
- **Requires healthcare professional validation** for all treatment decisions and medication protocols.

---

## 👨‍💻 Developer & Credits

- **💡 Idea & Developer**: Mahima Paseda Kusumsiri
- **🇱🇰 Made in**: Sri Lanka
- **📄 License**: MIT License
