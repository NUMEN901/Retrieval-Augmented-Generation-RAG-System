import os
import json
import fitz  # PyMuPDF for PDF text extraction
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import DATA_FOLDER, PROCESSED_FILE

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text_data = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            text_data.append({"page": page_num + 1, "content": text})

    return text_data

def process_pdfs():
    """Processes all PDFs and stores extracted text in chunks."""
    processed_chunks = []
    existing_pdfs = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]

    for pdf in existing_pdfs:
        book_title = pdf.replace(".pdf", "")
        pdf_path = os.path.join(DATA_FOLDER, pdf)

        extracted_text = extract_text_from_pdf(pdf_path)
        full_text = " ".join([page["content"] for page in extracted_text])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=500, separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(full_text)

        for idx, chunk in enumerate(chunks):
            processed_chunks.append({
                "book": book_title,
                "chunk_id": f"{book_title}_chunk_{idx}",
                "text": chunk,
                "metadata": {"source": book_title}
            })

    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_chunks, f, indent=4, ensure_ascii=False)

    return processed_chunks
