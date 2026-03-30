import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path, file_name):
    file_name = file_name.lower()

    if file_name.endswith(".pdf"):
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_name.endswith(".docx"):
        from docx import Document
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError("Unsupported file format")