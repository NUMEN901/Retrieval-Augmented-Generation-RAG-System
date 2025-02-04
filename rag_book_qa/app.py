import os
import sys

# Ensure 'src' is recognized
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import json
import streamlit as st
from dotenv import load_dotenv
from src.pdf_processor import process_pdfs
from src.embeddings import generate_embeddings, load_faiss_index
from src.retrieval import retrieve_relevant_chunks
from src.gpt_answer import generate_gpt_answer


# Load environment variables
load_dotenv()

print("DEBUG: OpenAI API Key:", os.getenv("OPENAI_API_KEY"))  



# Define folders
DATA_FOLDER = "data"

# Ensure necessary folders exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

st.title("📚 PDF Knowledge Assistant")

# 📌 Sidebar: PDF Upload
st.sidebar.header("📂 Upload Your PDFs")
uploaded_files = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# Save uploaded PDFs
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
        if os.path.exists(file_path):
            st.sidebar.warning(f"⚠️ {uploaded_file.name} already exists. Skipping...")
        else:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")

# Display existing PDFs
existing_pdfs = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
if existing_pdfs:
    st.sidebar.subheader("📜 Existing PDFs:")
    for pdf in existing_pdfs:
        st.sidebar.write(f"✅ {pdf}")

# 📌 Process PDFs & Generate Embeddings
if st.sidebar.button("📖 Process PDFs & Generate Embeddings"):
    if existing_pdfs:
        st.sidebar.info("🔄 Processing PDFs...")
        process_pdfs()
        st.sidebar.success("✅ PDF Processing Complete!")

        st.sidebar.info("🔄 Generating Embeddings...")
        if generate_embeddings():
            st.sidebar.success("✅ Embeddings Generated Successfully!")
        else:
            st.sidebar.error("❌ Failed to Generate Embeddings.")
    else:
        st.sidebar.error("❌ No PDFs found. Please upload files first.")

# Load FAISS index
index, metadata = load_faiss_index()
if index is None or metadata is None:
    st.error("❌ FAISS index not found. Please generate embeddings first.")
    st.stop()

st.subheader("🔍 Ask a Question About the PDFs")
query = st.text_input("Type your question here...")
if st.button("Get Answer"):
    if query:
        retrieved_texts = retrieve_relevant_chunks(query, index, metadata)
        final_answer = generate_gpt_answer(query, retrieved_texts)
        st.subheader("🤖 AI Answer:")
        st.write(final_answer)
    else:
        st.warning("⚠️ Please enter a question.")
