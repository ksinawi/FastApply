import io

import pytest
from docx import Document
from reportlab.pdfgen import canvas

from services.document_parser import extract_text


def _pdf(text: str) -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 720, text)
    pdf.save()
    return buffer.getvalue()


def test_pdf():
    assert "Jane Doe" in extract_text("resume.PDF", _pdf("Jane Doe - Python developer"))


def test_docx_includes_tables():
    document = Document()
    document.add_paragraph("Jane Doe")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Skills"
    table.cell(0, 1).text = "Python"
    buffer = io.BytesIO()
    document.save(buffer)

    text = extract_text("resume.docx", buffer.getvalue())
    assert "Jane Doe" in text and "Python" in text


def test_txt():
    assert extract_text("a.txt", b"hello") == "hello"


@pytest.mark.parametrize("name", ["resume.png", "resume", ""])
def test_unsupported_type(name):
    with pytest.raises(ValueError, match="PDF, DOCX, or TXT"):
        extract_text(name, b"data")


def test_corrupt_pdf():
    with pytest.raises(ValueError, match="couldn't read"):
        extract_text("resume.pdf", b"not a pdf")


def test_empty_text():
    with pytest.raises(ValueError, match="couldn't find any text"):
        extract_text("a.txt", b"   \n ")
