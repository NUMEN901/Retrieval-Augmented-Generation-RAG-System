import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import PROCESSED_FILE, FAISS_INDEX_FILE, METADATA_FILE

def generate_embeddings():
    """Generates FAISS embeddings and stores metadata."""
    if not os.path.exists(PROCESSED_FILE):
        return False

    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed_chunks = json.load(f)

    if not processed_chunks:
        return False

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in processed_chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    metadata = [{"book": chunk["metadata"]["source"], "chunk_id": chunk["chunk_id"], "text": chunk["text"]} for chunk in processed_chunks]

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    return True

def load_faiss_index():
    """Loads FAISS index and metadata."""
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(METADATA_FILE):
        return None, None

    index = faiss.read_index(FAISS_INDEX_FILE)

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata
