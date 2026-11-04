"""Document ingestion and extraction service for PDF documents and medical images."""

from io import BytesIO
import logging
from PIL import Image

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for extracting and pre-processing document text and images."""

    @classmethod
    def extract_text_from_pdf(cls, file_bytes: bytes) -> str:
        """Extracts text from a digital PDF file using modern PDF reader."""
        if not file_bytes:
            raise ValueError("Empty PDF file data provided.")

        try:
            reader = PdfReader(BytesIO(file_bytes))
            extracted_pages = []

            for page_index, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text.strip())

            full_text = "\n\n".join(extracted_pages).strip()

            if not full_text:
                raise ValueError(
                    "This PDF appears to be a scanned image or photograph of a report without selectable text. "
                    "Please upload a photo/image directly or copy-paste the text."
                )

            return full_text

        except Exception as exc:
            if "scanned image" in str(exc):
                raise
            logger.error("PDF extraction error: %s", exc)
            raise ValueError(f"Failed to read PDF document: {exc}") from exc

    @classmethod
    def optimize_image_for_ocr(cls, image_bytes: bytes, max_dimension: int = 2400) -> bytes:
        """Optimizes and resizes medical report photos/scans for OCR stability."""
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                # Convert color spaces like CMYK/RGBA to RGB
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Resize if image exceeds maximum dimension to prevent OCR timeouts
                width, height = img.size
                if max(width, height) > max_dimension:
                    scale = max_dimension / max(width, height)
                    new_size = (int(width * scale), int(height * scale))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                output_buffer = BytesIO()
                img.save(output_buffer, format="JPEG", quality=85, optimize=True)
                return output_buffer.getvalue()
        except Exception as exc:
            logger.warning("Image optimization fallback: using raw bytes (%s)", exc)
            return image_bytes

