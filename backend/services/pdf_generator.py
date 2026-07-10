from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_resume_pdf(tailored_content: str):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    for line in tailored_content.split("\n"):
        if line.strip():
            elements.append(Paragraph(line, styles["Normal"]))


    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf