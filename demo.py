from vectorization import Vectorizer
from faiss_index import FaissIndex

# STEP 1: chunks
chunks = [
    {"chunk_id": 1, "text": "The party shall be liable for damages.", "type": "liability"},
    {"chunk_id": 2, "text": "This agreement may be terminated anytime.", "type": "termination"},
]

# STEP 2: embeddings
vec = Vectorizer()
embedded_chunks = vec.encode_chunks(chunks)

# STEP 3: FAISS index
faiss_db = FaissIndex()

# build index
faiss_db.build_index(embedded_chunks)

# STEP 4: query
query = "Who is responsible for damages?"
query_embedding = vec.model.encode(query)

results = faiss_db.search(query_embedding, top_k=2)

print("\n[SEARCH RESULTS]")
for r in results:
    print(r)

from llm import LLM

llm = LLM()

# Summary
summary = llm.generate_summary(chunks)
print(summary)

# RAG Answer
answer = llm.generate_answer("Who is liable?", results)
print(answer)