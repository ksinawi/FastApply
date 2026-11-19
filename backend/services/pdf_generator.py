"""Resume PDF rendering.

A compact, ATS-friendly single-column layout (Education, Experience, Projects,
Technical Skills). The resume is rendered at progressively tighter sizes until it
fits on one page; only genuinely long resumes spill onto a second page.
"""
import re
from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from schemas.resume import Resume, SkillGroup
from services.pdf_styles import esc

TEXT = colors.HexColor("#111111")
MUTED = colors.HexColor("#4A4A4A")
RULE = colors.HexColor("#9A9A9A")

# Tried in order until the resume fits on one page.
FIT_SCALES = (1.0, 0.96, 0.92, 0.88, 0.85, 0.82)
DATE_COLUMN = 1.45 * inch


@dataclass
class _Styles:
    scale: float

    def __post_init__(self):
        s = self.scale
        self.name = ParagraphStyle("Name", fontName="Helvetica-Bold", fontSize=18 * s, leading=21 * s,
                                   alignment=TA_CENTER, textColor=TEXT, spaceAfter=3 * s)
        self.contact = ParagraphStyle("Contact", fontName="Helvetica", fontSize=9 * s, leading=11.5 * s,
                                      alignment=TA_CENTER, textColor=MUTED, spaceAfter=4 * s)
        self.section = ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=10.5 * s, leading=12 * s,
                                      textColor=TEXT, spaceBefore=7 * s, spaceAfter=1 * s)
        self.left = ParagraphStyle("Left", fontName="Helvetica", fontSize=10 * s, leading=12.5 * s, textColor=TEXT)
        self.right = ParagraphStyle("Right", parent=self.left, fontSize=9.5 * s, alignment=TA_RIGHT, textColor=MUTED)
        self.sub = ParagraphStyle("Sub", parent=self.left, fontName="Helvetica-Oblique", fontSize=9.5 * s,
                                  textColor=MUTED)
        self.body = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5 * s, leading=12 * s, textColor=TEXT,
                                   spaceAfter=1.5 * s)
        self.bullet = ParagraphStyle("Bullet", parent=self.body, leftIndent=12 * s, bulletIndent=3 * s,
                                     bulletFontSize=8 * s)
        self.entry_gap = 5 * s
        self.rule_gap = 3 * s
        self.margin_x = max(0.5 * s, 0.42) * inch
        self.margin_y = max(0.45 * s, 0.38) * inch


def _date_range(start: str, end: str) -> str:
    start, end = (start or "").strip(), (end or "").strip()
    if start and end and start.lower() == end.lower():
        return start
    return " – ".join(part for part in (start, end) if part)


def _clean_link(link: str) -> str:
    return re.sub(r"^(https?://)?(www\.)?", "", link.strip()).rstrip("/")


def _section(title: str, st: _Styles) -> list:
    return [
        Paragraph(esc(title).upper(), st.section),
        HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=0, spaceAfter=st.rule_gap),
    ]


def _row_table(rows: list[tuple[Paragraph, Paragraph | str]], width: float) -> Table:
    table = Table([list(row) for row in rows], colWidths=[width - DATE_COLUMN, DATE_COLUMN])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def _bullets(items: list[str], st: _Styles) -> list:
    return [Paragraph(esc(item.strip()), st.bullet, bulletText="•") for item in items if item and item.strip()]


def _skill_groups(resume: Resume) -> list[SkillGroup]:
    groups = [group for group in resume.skill_groups if group.category.strip() and group.skills]
    if groups:
        return groups
    return [SkillGroup(category="Skills", skills=resume.skills)] if resume.skills else []


def _story(resume: Resume, st: _Styles, width: float) -> list:
    story = []
    contact = resume.contact_info

    if contact.name:
        story.append(Paragraph(esc(contact.name), st.name))

    parts = [contact.location, contact.phone, contact.email, *(_clean_link(link) for link in contact.links)]
    parts = [esc(part) for part in parts if part and part.strip()]
    if parts:
        story.append(Paragraph("  |  ".join(parts), st.contact))

    if resume.education:
        story += _section("Education", st)
        for edu in resume.education:
            rows = [(Paragraph(f"<b>{esc(edu.degree)}</b>", st.left),
                     Paragraph(esc(_date_range(edu.start_date, edu.end_date)), st.right))]
            if edu.institution:
                rows.append((Paragraph(esc(edu.institution), st.sub), ""))
            block = [_row_table(rows, width)]
            if edu.relevant_courses:
                block.append(Paragraph(
                    f"<b>Relevant Coursework:</b> {esc(', '.join(edu.relevant_courses))}", st.body))
            story.append(KeepTogether(block))
            story.append(Spacer(1, st.entry_gap))

    if resume.experience:
        story += _section("Experience", st)
        for exp in resume.experience:
            rows = [(Paragraph(f"<b>{esc(exp.title)}</b>", st.left),
                     Paragraph(esc(_date_range(exp.start_date, exp.end_date)), st.right))]
            if exp.company:
                rows.append((Paragraph(esc(exp.company), st.sub), ""))
            story.append(KeepTogether([_row_table(rows, width), *_bullets(exp.responsibilities, st)]))
            story.append(Spacer(1, st.entry_gap))

    if resume.projects:
        story += _section("Projects", st)
        for proj in resume.projects:
            title = f"<b>{esc(proj.name)}</b>"
            if proj.technologies:
                title += f" <font color='#9A9A9A'>|</font> <i>{esc(', '.join(proj.technologies))}</i>"
            rows = [(Paragraph(title, st.left), Paragraph(esc(_date_range(proj.start_date, proj.end_date)), st.right))]
            story.append(KeepTogether([_row_table(rows, width), *_bullets(proj.description, st)]))
            story.append(Spacer(1, st.entry_gap))

    groups = _skill_groups(resume)
    if groups:
        story += _section("Technical Skills", st)
        for group in groups:
            story.append(Paragraph(f"<b>{esc(group.category)}:</b> {esc(', '.join(group.skills))}", st.body))

    return story


def _render(resume: Resume, scale: float) -> bytes:
    st = _Styles(scale)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=LETTER,
        leftMargin=st.margin_x, rightMargin=st.margin_x, topMargin=st.margin_y, bottomMargin=st.margin_y,
        title=f"{resume.contact_info.name} Resume".strip(), author=resume.contact_info.name,
    )
    # SimpleDocTemplate's frame adds 6pt padding on each side; size tables to the usable width.
    doc.build(_story(resume, st, doc.width - 12))
    return buffer.getvalue()


def _page_count(pdf: bytes) -> int:
    return len(PdfReader(BytesIO(pdf)).pages)


def generate_resume_pdf(resume: Resume) -> bytes:
    pdf = b""
    for scale in FIT_SCALES:
        pdf = _render(resume, scale)
        if _page_count(pdf) == 1:
            return pdf
    return pdf  # genuinely too long for one page: smallest version, on two pages
