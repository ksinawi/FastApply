from io import BytesIO

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from schemas.resume import Resume
from services.pdf_styles import (
    BODY_STYLE,
    BULLET_STYLE,
    DATE_STYLE,
    ENTRY_TITLE_STYLE,
    RULE_COLOR,
    SECTION_STYLE,
    esc,
)
from services.pdf_styles import CONTACT_STYLE, NAME_STYLE


def _section_header(title: str) -> list:
    return [
        Paragraph(esc(title).upper(), SECTION_STYLE),
        HRFlowable(width="100%", thickness=0.75, color=RULE_COLOR, spaceAfter=6),
    ]


def _date_range(start: str, end: str) -> str:
    return " - ".join(p for p in [start, end] if p)


def _entry_header(title: str, subtitle: str, date_range: str) -> Table:
    heading = esc(title)

    if subtitle:
        heading += f"<br/><font name='Helvetica-Oblique' size='9.5' color='#333333'>{esc(subtitle)}</font>"

    left = Paragraph(heading, ENTRY_TITLE_STYLE)
    right = Paragraph(esc(date_range), DATE_STYLE)

    table = Table([[left, right]], colWidths=[5.5 * inch, 1.7 * inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return table


def _bullets(items: list[str]) -> list:
    return [
        Paragraph(f"&bull;&nbsp; {esc(item)}", BULLET_STYLE)
        for item in items
        if item and item.strip()
    ]


def generate_resume_pdf(resume: Resume) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    elements = []

    contact = resume.contact_info

    if contact.name:
        elements.append(Paragraph(esc(contact.name), NAME_STYLE))

    contact_parts = [p for p in [contact.location, contact.email, contact.phone, *contact.links] if p]
    if contact_parts:
        elements.append(Paragraph(" &nbsp;|&nbsp; ".join(esc(p) for p in contact_parts), CONTACT_STYLE))

    if resume.skills:
        elements += _section_header("Skills")
        elements.append(Paragraph(esc(", ".join(resume.skills)), BODY_STYLE))

    if resume.experience:
        elements += _section_header("Experience")
        for exp in resume.experience:
            elements.append(_entry_header(exp.title, exp.company, _date_range(exp.start_date, exp.end_date)))
            elements += _bullets(exp.responsibilities)
            elements.append(Spacer(1, 6))

    if resume.projects:
        elements += _section_header("Projects")
        for proj in resume.projects:
            subtitle = ", ".join(proj.technologies)
            elements.append(_entry_header(proj.name, subtitle, _date_range(proj.start_date, proj.end_date)))
            elements += _bullets(proj.description)
            elements.append(Spacer(1, 6))

    if resume.education:
        elements += _section_header("Education")
        for edu in resume.education:
            elements.append(_entry_header(edu.degree, edu.institution, _date_range(edu.start_date, edu.end_date)))
            if edu.relevant_courses:
                elements.append(Paragraph(
                    f"<font color='#555555'>Relevant coursework:</font> {esc(', '.join(edu.relevant_courses))}",
                    BODY_STYLE,
                ))
            elements.append(Spacer(1, 6))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
