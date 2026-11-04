import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration management."""
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.getenv("SECRET_KEY", "lankamedi-ai-dev-secret-key-2026")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("PORT", "5000"))

    # Uploads & Document Processing
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "16")) * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}
    ALLOWED_DOC_EXTENSIONS = {".pdf"}
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOC_EXTENSIONS

    # Provider 1: NVIDIA NIM
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "").strip()
    NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").rstrip("/")
    NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-bolt-e4b").strip()

    # Provider 2: Google Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

    # Provider 3: OpenAI / Groq / Ollama
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    # OCR Providers
    OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY", "").strip()

    # Request Timeouts (in seconds)
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "45"))
    OCR_TIMEOUT = int(os.getenv("OCR_TIMEOUT", "30"))

    @classmethod
    def get_active_providers(cls):
        """Returns a list of actively configured LLM and OCR providers."""
        providers = []
        if cls.NVIDIA_API_KEY:
            providers.append(f"NVIDIA NIM ({cls.NVIDIA_MODEL})")
        if cls.GEMINI_API_KEY:
            providers.append(f"Google Gemini ({cls.GEMINI_MODEL})")
        if cls.OPENAI_API_KEY:
            providers.append(f"OpenAI/Compatible ({cls.OPENAI_MODEL})")
        return providers

