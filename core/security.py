"""Security, input validation, and patient health information (PII/PHI) de-identification."""

import re
from pathlib import Path
from werkzeug.utils import secure_filename
from core.config import Config


# Regular expressions for Sri Lankan identification and sensitive contact patterns
SL_NIC_PATTERN = re.compile(r"\b(?:\d{9}[vVxX]|\d{12})\b")
SL_PHONE_PATTERN = re.compile(
    r"\b(?:\+94|0094|0)\s*(?:7[01245678]|11|21|23|24|25|26|27|31|32|33|34|35|36|37|38|41|45|47|51|52|54|55|57|63|65|66|67)\s*\d{3}\s*\d{4}\b"
)
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# Common Sri Lankan laboratory header prefixes for patient demographics
PATIENT_NAME_PATTERNS = [
    re.compile(r"(?i)(?:patient\s*name|pt\s*name|name)\s*[:\-]\s*([A-Za-z\s\.]+)(?=\n|\r|,|;|\t|Age|Gender|Sex|Ref)"),
    re.compile(r"(?i)\b(?:Mr\.|Mrs\.|Ms\.|Miss|Master|Dr\.|Rev\.)\s+[A-Za-z\s\.]+(?=\n|\r|,|;|\t|Age|Gender|Sex)"),
]


class PIIScrubber:
    """De-identifies sensitive patient identifiers before external processing."""

    @classmethod
    def redact_text(cls, text: str) -> str:
        """Sanitizes sensitive personal identifiers from medical report text."""
        if not text:
            return ""

        redacted = text

        # 1. Redact Sri Lankan National Identity Card (NIC) numbers
        redacted = SL_NIC_PATTERN.sub("[REDACTED_NIC]", redacted)

        # 2. Redact Phone numbers
        redacted = SL_PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)

        # 3. Redact Emails
        redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)

        # 4. Redact Patient Name fields from lab headers
        for pattern in PATIENT_NAME_PATTERNS:
            redacted = pattern.sub("Patient Name: [REDACTED_NAME]", redacted)

        return redacted


class FileSecurityValidator:
    """Validates uploaded files for type, extension, size, and magic bytes."""

    MAGIC_SIGNATURES = {
        ".pdf": b"%PDF",
        ".png": b"\x89PNG\r\n\x1a\n",
        ".jpg": b"\xff\xd8\xff",
        ".jpeg": b"\xff\xd8\xff",
        ".webp": b"RIFF",
        ".bmp": b"BM",
        ".tiff": (b"II*\x00", b"MM\x00*"),
    }

    @classmethod
    def validate_file(cls, filename: str, file_bytes: bytes) -> tuple[bool, str]:
        """Validates filename extension, byte size, and header signature."""
        if not filename:
            return False, "No file provided"

        clean_name = secure_filename(filename)
        ext = Path(clean_name).suffix.lower()

        if ext not in Config.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file extension '{ext}'. Allowed: PDF, PNG, JPG, JPEG, WEBP, BMP, TIFF."

        if len(file_bytes) == 0:
            return False, "Uploaded file is empty."

        if len(file_bytes) > Config.MAX_CONTENT_LENGTH:
            return False, f"File exceeds maximum allowed size of {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB."

        # Verify magic byte signature
        expected_magic = cls.MAGIC_SIGNATURES.get(ext)
        if expected_magic:
            if isinstance(expected_magic, tuple):
                if not any(file_bytes.startswith(sig) for sig in expected_magic):
                    return False, f"File header signature does not match valid {ext} format."
            else:
                if not file_bytes.startswith(expected_magic):
                    return False, f"File header signature does not match valid {ext} format."

        return True, "Valid"

