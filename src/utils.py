import pdfplumber

def load_document(path):
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)
