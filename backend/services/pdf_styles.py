from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

TEXT_COLOR = colors.HexColor("#1A1A1A")
MUTED_COLOR = colors.HexColor("#555555")
RULE_COLOR = colors.HexColor("#CCCCCC")

NAME_STYLE = ParagraphStyle(
    "Name", fontName="Helvetica-Bold", fontSize=20, leading=24,
    alignment=TA_CENTER, textColor=TEXT_COLOR, spaceAfter=4,
)
CONTACT_STYLE = ParagraphStyle(
    "Contact", fontName="Helvetica", fontSize=9, leading=12,
    alignment=TA_CENTER, textColor=MUTED_COLOR, spaceAfter=10,
)
SECTION_STYLE = ParagraphStyle(
    "Section", fontName="Helvetica-Bold", fontSize=11, leading=14,
    textColor=TEXT_COLOR, spaceBefore=10, spaceAfter=2,
)
ENTRY_TITLE_STYLE = ParagraphStyle(
    "EntryTitle", fontName="Helvetica-Bold", fontSize=10, leading=15,
    textColor=TEXT_COLOR,
)
DATE_STYLE = ParagraphStyle(
    "Date", fontName="Helvetica", fontSize=9, leading=15,
    alignment=TA_RIGHT, textColor=MUTED_COLOR,
)
BODY_STYLE = ParagraphStyle(
    "Body", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=TEXT_COLOR, spaceAfter=4,
)
BULLET_STYLE = ParagraphStyle(
    "Bullet", parent=BODY_STYLE, leftIndent=14, spaceAfter=2,
)


def esc(text: str) -> str:
    return escape(text or "")
