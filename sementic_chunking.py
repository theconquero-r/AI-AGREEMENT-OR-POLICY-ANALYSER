import torch.nn.functional as F
import os
# os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
# os.environ["HF_HUB_OFFLINE"] = "1"
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# import logging
# logging.getLogger("transformers").setLevel(logging.ERROR)

CLAUSE_KEYWORDS = {

    "termination": [
        "terminate", "termination", "end agreement", "breach",
        "cancel", "cancellation", "expiry", "expire", "notice period"
    ],

    "liability": [
        "liable", "liability", "damages", "loss",
        "responsible", "responsibility", "risk",
        "limitation of liability", "indirect damages", "consequential damages"
    ],

    "confidentiality": [
        "confidential", "non-disclosure", "nda", "private",
        "sensitive information", "proprietary", "secret",
        "data protection", "data privacy"
    ],

    "payment": [
        "payment", "invoice", "fee", "amount", "due",
        "charges", "cost", "price", "compensation",
        "installment", "milestone", "billing", "late fee", "penalty"
    ],

    "indemnity": [
        "indemnify", "indemnity", "hold harmless",
        "defend", "claims", "third-party claims"
    ],

    "governing_law": [
        "law", "jurisdiction", "court",
        "governing law", "applicable law", "legal jurisdiction"
    ],

    "dispute": [
        "dispute", "arbitration", "resolution",
        "settlement", "mediation", "conflict"
    ],

    # 🔥 NEW (VERY IMPORTANT)
    "ownership": [
        "ownership", "intellectual property", "ip",
        "rights", "ownership rights", "transfer of ownership",
        "assign", "assignment", "assign rights",
        "copyright", "trademark", "license", "licensing",
        "retain rights", "work product", "deliverables",
        "proprietary rights"
    ],

    # 🔥 BONUS (VERY POWERFUL)
    "warranty": [
        "warranty", "guarantee", "assurance",
        "no guarantee", "no warranty", "as is",
        "disclaimer"
    ],

    "delivery": [
        "delivery", "timeline", "deadline",
        "milestone", "submission", "completion",
        "within days", "schedule"
    ]
}


import re

def get_category(sentence):
    sentence = sentence.lower()

    for category, keywords in CLAUSE_KEYWORDS.items():
        for word in keywords:
            if word in sentence:
                return category

    return "other"

def is_section_header(sentence):
    sentence = sentence.lower()

    SECTION_HEADERS = [
        "scope of services",
        "payment",
        "intellectual property",
        "ownership",
        "confidentiality",
        "termination",
        "liability",
        "dispute",
        "governing law",
        "warranty",
        "delivery"
    ]

    return any(header in sentence for header in SECTION_HEADERS)

def split_into_sentences(text):
    """
    Basic sentence splitter using regex.
    Handles ., ?, ! as sentence boundaries.
    """
    if not text:
        return []

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Split sentences
    sentences = re.split(r'(?<=[.?!])\s+', text)

    # Clean sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2',device="cuda" if torch.cuda.is_available() else "cpu")


def get_embeddings(sentences):
    return model.encode(
        sentences,
        batch_size=64,
        show_progress_bar=False,
        convert_to_tensor=True   # 🔥 MUST for GPU
    )



def compute_similarity(vec1, vec2):
    return F.cosine_similarity(vec1, vec2, dim=0).item()


def hybrid_chunking(sentences, threshold=0.6):
    embeddings = get_embeddings(sentences)

    chunks = []
    current_chunk = [sentences[0]]
    current_embeddings = [embeddings[0]]
    current_category = get_category(sentences[0])

    chunk_id = 1

    for i in range(1, len(sentences)):
        curr_sentence = sentences[i]
        curr_embedding = embeddings[i]
        curr_category = get_category(curr_sentence)

        # 🔥 NEW: FORCE SPLIT ON HEADER
        if is_section_header(curr_sentence):
            chunks.append({
                "chunk_id": chunk_id,
                "text": " ".join(current_chunk),
                "type": current_category
                })

            chunk_id += 1
            current_chunk = [curr_sentence]
            current_embeddings = [curr_embedding]
            current_category = curr_category
            continue

        centroid = sum(current_embeddings) / len(current_embeddings)
        similarity = compute_similarity(centroid, curr_embedding)

        # 🔥 HYBRID DECISION
        if similarity >= threshold or curr_category == current_category:
            current_chunk.append(curr_sentence)
            current_embeddings.append(curr_embedding)
        else:
            chunks.append({
                "chunk_id": chunk_id,
                "text": " ".join(current_chunk),
                "type": current_category
            })

            chunk_id += 1
            current_chunk = [curr_sentence]
            current_embeddings = [curr_embedding]
            current_category = curr_category

    # last chunk
    if current_chunk:
        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(current_chunk),
            "type": current_category
        })

    return chunks

# 🔥 TEST
if __name__ == "__main__":
    sentences = [
        "This agreement shall terminate if either party breaches the contract.",
        "Either party may end the agreement in case of violation.",
        "The company is not liable for any indirect damages.",
        "No party shall be responsible for financial losses."
    ]

    chunks = hybrid_chunking(sentences, threshold=0.6)

    for chunk in chunks:
        print(chunk)
        print("-" * 50)