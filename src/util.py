import glob
import os
from typing import Optional, List

import fitz  # PyMuPDF
from pydantic import BaseModel, FilePath, DirectoryPath


class PDFListRequest(BaseModel):
    directory: DirectoryPath


class PDFListResponse(BaseModel):
    pdf_files: List[str]


def list_pdf_files(request: PDFListRequest) -> PDFListResponse:
    """
    Use glob to recursively find all PDF files in the directory and subdirectories
    """
    pdf_files = glob.glob(os.path.join(request.directory, '**', '*.pdf'), recursive=True)
    return PDFListResponse(pdf_files=pdf_files)


class PDFTextExtractionRequest(BaseModel):
    pdf_path: FilePath


class PDFTextExtractionResponse(BaseModel):
    text: str
    error: Optional[str] = None


def extract_text_from_pdf(request: PDFTextExtractionRequest) -> PDFTextExtractionResponse:
    try:
        # Open the PDF file
        document = fitz.open(request.pdf_path)

        # Initialize a string to hold all text
        full_text = ""

        # Iterate over each page
        for page_num in range(len(document)):
            page = document.load_page(page_num)  # Load the page
            text = page.get_text("text")  # Extract text
            full_text += text

        return PDFTextExtractionResponse(text=full_text)

    except Exception as e:
        return PDFTextExtractionResponse(text="", error=str(e))
