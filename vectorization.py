# vectorization.py

from sentence_transformers import SentenceTransformer
import torch
import os
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

class Vectorizer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Using device: {self.device}")

        self.model = SentenceTransformer(model_name, device=self.device)

    def encode_chunks(self, chunks, batch_size=16):
        """
        Convert chunks into embeddings

        Args:
            chunks (list): list of dicts
            batch_size (int): batch size for encoding

        Returns:
            list: embedded chunks with metadata
        """

        if not chunks:
            return []

        texts = [chunk["text"] for chunk in chunks]

        print("[INFO] Generating embeddings...")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=True,
            show_progress_bar=True
        )

        embedded_chunks = []

        for i, chunk in enumerate(chunks):
            embedded_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "type": chunk.get("type", "unknown"),
                "embedding": embeddings[i].cpu().numpy()
            })

        return embedded_chunks


