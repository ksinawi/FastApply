import io

from PyPDF2 import PdfReader
from docx import Document

def _extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

def _extract_docx_text(file_bytes: bytes) -> str:
    document = Document(io.BytesIO(file_bytes))

    return "\n".join(paragraph.text for paragraph in document.paragraphs)

def _extract_txt_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")

def extract_text(filename: str, file_bytes: bytes) -> str:
    extension = (filename or "").rsplit(".", 1)[-1].lower()

    if extension == "pdf":
        return _extract_pdf_text(file_bytes)

    if extension == "docx":
        return _extract_docx_text(file_bytes)

    if extension == "txt":
        return _extract_txt_text(file_bytes)

    raise ValueError(f"Unsupported file type: .{extension}")
