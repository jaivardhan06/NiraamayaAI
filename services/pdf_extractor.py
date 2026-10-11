import pdfplumber
import pymupdf
import io

def extract_text_pdfplumber(file_bytes: bytes) -> str:
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            text += " | ".join(
                                [str(cell) if cell else "" for cell in row]
                            ) + "\n"
        return text.strip()
    except Exception as e:
        print(f"pdfplumber failed: {e}")
        return ""

def extract_text_pymupdf(file_bytes: bytes) -> str:
    try:
        text = ""
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        return ""

def extract_text(file_bytes: bytes) -> str:
    """
    Try pdfplumber first
    Fallback to PyMuPDF if fails
    """
    text = extract_text_pdfplumber(file_bytes)
    if len(text) < 100:
        print("Switching to PyMuPDF...")
        text = extract_text_pymupdf(file_bytes)
    return text