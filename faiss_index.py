# faiss_index.py

import faiss
import numpy as np


class FaissIndex:
    def __init__(self, dim=384):
        """
        dim = embedding dimension (MiniLM = 384)
        """
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)  # simple & fast
        self.metadata = []  # store chunks info

    def build_index(self, embedded_chunks):
        """
        embedded_chunks: output from vectorizer
        """

        if not embedded_chunks:
            print("[WARNING] No chunks to index")
            return

        vectors = []
        self.metadata = []

        for chunk in embedded_chunks:
            vectors.append(chunk["embedding"])
            self.metadata.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "type": chunk["type"]
            })

        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)

        print(f"[INFO] Indexed {len(vectors)} chunks")

    def search(self, query_embedding, top_k=5):
        """
        query_embedding: numpy array
        """

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

    def reset(self):
        """
        Clear old index (for new file)
        """
        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata = []
        print("[INFO] FAISS index reset")