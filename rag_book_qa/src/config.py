import os

DATA_FOLDER = "data"
PROCESSED_FILE = os.path.join(DATA_FOLDER, "processed_chunks.json")
FAISS_INDEX_FILE = os.path.join("embeddings", "vector_index.faiss")
METADATA_FILE = os.path.join("embeddings", "metadata.json")
