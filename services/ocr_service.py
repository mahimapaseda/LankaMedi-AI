"""Optical Character Recognition (OCR) service for processing medical report images."""

import base64
import logging
import requests
from core.config import Config
from services.document_service import DocumentService

logger = logging.getLogger(__name__)


class OCRService:
    """Service to process medical report images via cloud OCR with optimizations."""

    @classmethod
    def extract_text(cls, image_bytes: bytes) -> str:
        """Extracts text from medical report image bytes."""
        if not image_bytes:
            raise ValueError("No image data provided for OCR.")

        # Pre-process & optimize image size before upload
        optimized_bytes = DocumentService.optimize_image_for_ocr(image_bytes)
        image_b64 = base64.b64encode(optimized_bytes).decode("utf-8")

        api_key = Config.OCR_SPACE_API_KEY or "helloworld"

        payload = {
            "base64Image": f"data:image/jpeg;base64,{image_b64}",
            "apikey": api_key,
            "language": "eng",
            "isOverlayRequired": False,
            "OCREngine": "2",
            "scale": True,
            "isTable": True,
        }

        try:
            response = requests.post(
                "https://api.ocr.space/parse/image",
                data=payload,
                timeout=Config.OCR_TIMEOUT,
            )
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.Timeout:
            raise ValueError(
                "OCR processing timed out. Please try uploading a cropped, higher-contrast image or copy-paste the text directly."
            )
        except requests.RequestException as exc:
            logger.error("OCR API network failure: %s", exc)
            raise ValueError(f"OCR request failed: {exc}") from exc

        if result.get("IsErroredOnProcessing"):
            msg = result.get("ErrorMessage") or result.get("ErrorDetails") or "OCR processing failed"
            if isinstance(msg, list):
                msg = "; ".join(str(m) for m in msg)
            raise ValueError(f"OCR Error: {msg}")

        parsed_results = result.get("ParsedResults") or []
        if not parsed_results:
            raise ValueError("OCR could not recognize text in this image. Please upload a clearer photograph.")

        extracted = (parsed_results[0].get("ParsedText") or "").strip()
        if not extracted:
            raise ValueError("OCR produced empty text. Ensure the medical document is in focus, well-lit, and legible.")

        return extracted

