import io
from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text(file_uploaded):
    """
    Routes the file to the correct extractor based on file extension.
    """
    file_type = file_uploaded.name.split('.')[-1].lower()
    
    try:
        if file_type == 'pdf':
            return extract_text_from_pdf(file_uploaded)
        elif file_type == 'docx':
            return extract_text_from_docx(file_uploaded)
    except Exception as e:
        print(f"Error parsing {file_uploaded.name}: {e}")
        return None

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file using pdfminer.
    """
    # Create a BytesIO object from the uploaded file
    file_bytes = io.BytesIO(file.read())
    text = extract_pdf_text(file_bytes)
    return text

def extract_text_from_docx(file):
    """
    Extracts text from a DOCX file using python-docx.
    """
    file_bytes = io.BytesIO(file.read())
    doc = docx.Document(file_bytes)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)