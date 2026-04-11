from pathlib import Path
from PyPDF2 import PdfReader

# Extract from txt format
def extract_text_from_txt(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"{file_path} does not exist")
    
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


# Extract from pdf format
def extract_text_from_pdf(file_path: str)-> str:
    reader = PdfReader(file_path)
    
    text = ""
    for page in reader.pages():
        text += page.extract_text() + "\n"
    
    return text


# function to call from ingestion route
def extract_text(file_path: str) -> str:
    if file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)

    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    
    else:
        raise ValueError("Unsupported file type")






