import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query, index, metadata, k=10):
    """Retrieves the most relevant text chunks for a given query."""
    query_embedding = model.encode([query], convert_to_numpy=True)

    # ✅ Ensure the query embedding has the correct shape
    query_embedding = np.array(query_embedding).reshape(1, -1)

    # ✅ Perform FAISS search
    distances, indices = index.search(query_embedding, k)

    retrieved_texts = []
    used_chunks = set()

    for i in range(len(indices[0])):
        idx = indices[0][i]
        if idx < len(metadata):  # Ensure valid index
            chunk_text = metadata[idx]["text"]

            # Ensure uniqueness in retrieval
            if chunk_text not in used_chunks:
                retrieved_texts.append(chunk_text)
                used_chunks.add(chunk_text)

    return retrieved_texts
