import io
import logging

from docx import Document
from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {"pdf", "docx", "txt"}


def _extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _extract_docx_text(file_bytes: bytes) -> str:
    document = Document(io.BytesIO(file_bytes))

    lines = [paragraph.text for paragraph in document.paragraphs]

    # Many resume templates put content in tables; don't drop it.
    for table in document.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text for cell in row.cells if cell.text.strip()))

    return "\n".join(lines)


def _extract_txt_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Extract plain text from an uploaded document. Raises ValueError with a user-facing message."""
    extension = (filename or "").rsplit(".", 1)[-1].lower() if "." in (filename or "") else ""

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type{f' .{extension}' if extension else ''}. Please upload a PDF, DOCX, or TXT file.")

    try:
        if extension == "pdf":
            text = _extract_pdf_text(file_bytes)
        elif extension == "docx":
            text = _extract_docx_text(file_bytes)
        else:
            text = _extract_txt_text(file_bytes)
    except (PdfReadError, ValueError, KeyError, OSError) as error:
        logger.info("Could not parse %s upload: %s", extension, error)
        raise ValueError("We couldn't read that file. It may be corrupted or password-protected.") from error
    except Exception as error:  # zipfile.BadZipFile and friends from python-docx
        logger.info("Could not parse %s upload: %s", extension, error)
        raise ValueError("We couldn't read that file. It may be corrupted or password-protected.") from error

    text = text.strip()

    if not text:
        raise ValueError("We couldn't find any text in that file. If it's a scanned PDF, try exporting it as a text-based PDF or DOCX.")

    return text
