from datetime import date
from io import BytesIO

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from schemas.cover_letter import CoverLetter
from services.pdf_styles import CONTACT_STYLE, MUTED_COLOR, NAME_STYLE, TEXT_COLOR, esc

LETTER_BODY_STYLE = ParagraphStyle(
    "LetterBody", fontName="Helvetica", fontSize=10.5, leading=16,
    textColor=TEXT_COLOR, spaceAfter=12,
)
DATE_LINE_STYLE = ParagraphStyle(
    "DateLine", fontName="Helvetica", fontSize=9.5, leading=14,
    textColor=MUTED_COLOR, spaceAfter=16,
)


def generate_cover_letter_pdf(cover_letter: CoverLetter) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
    )

    elements = []

    contact = cover_letter.contact_info

    if contact.name:
        elements.append(Paragraph(esc(contact.name), NAME_STYLE))

    contact_parts = [p for p in [contact.location, contact.email, contact.phone, *contact.links] if p]
    if contact_parts:
        elements.append(Paragraph(" &nbsp;|&nbsp; ".join(esc(p) for p in contact_parts), CONTACT_STYLE))

    elements.append(Paragraph(esc(date.today().strftime("%B %d, %Y")), DATE_LINE_STYLE))

    if cover_letter.recipient:
        elements.append(Paragraph(esc(cover_letter.recipient), LETTER_BODY_STYLE))

    if cover_letter.opening_paragraph:
        elements.append(Paragraph(esc(cover_letter.opening_paragraph), LETTER_BODY_STYLE))

    for paragraph in cover_letter.body_paragraphs:
        if paragraph and paragraph.strip():
            elements.append(Paragraph(esc(paragraph), LETTER_BODY_STYLE))

    if cover_letter.closing_paragraph:
        elements.append(Paragraph(esc(cover_letter.closing_paragraph), LETTER_BODY_STYLE))

    if cover_letter.signature:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(esc(cover_letter.signature).replace("\n", "<br/>"), LETTER_BODY_STYLE))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
