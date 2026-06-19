from PyPDF2 import PdfReader
import io

def extract_text(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text