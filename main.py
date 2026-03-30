# main.py

from pdf_and_docs_reader import extract_text
from text_cleaning import clean_text
from sementic_chunking import split_into_sentences, hybrid_chunking  

from vectorization import Vectorizer
from faiss_index import FaissIndex
from llm import LLM

class AgreementAnalyzer:
    def __init__(self):
        self.vectorizer = Vectorizer()
        self.faiss_db = FaissIndex()
        self.llm = LLM()

    def process_file(self, file_path,file_name=None):
        print("[INFO] Reading file...")
        if file_name is None:
            file_name=file_path
        raw_text = extract_text(file_path,file_name=file_name)

        print("[INFO] Cleaning text...")
        cleaned_text = clean_text(raw_text)

        print("[INFO] Splitting into sentences...")
        sentences = split_into_sentences(cleaned_text)

        print("[INFO] Performing hybrid chunking...")
        chunks = hybrid_chunking(sentences, threshold=0.6)

        print(f"[INFO] Total chunks: {len(chunks)}")

        print("[INFO] Vectorizing...")
        embedded_chunks = self.vectorizer.encode_chunks(chunks)

        print("[INFO] Building FAISS index...")
        self.faiss_db.reset()
        self.faiss_db.build_index(embedded_chunks)

        self.chunks = chunks  # store for summary

        return chunks

    def generate_summary(self):
        print("[INFO] Generating summary...")
        return self.llm.generate_summary(self.chunks)

    def chat(self):
        print("\n💬 Chat started (type 'exit' to quit)\n")

        while True:
            query = input("You: ")

            if query.lower() == "exit":
                break

            query_embedding = self.vectorizer.model.encode(query)

            results = self.faiss_db.search(query_embedding, top_k=3)

            answer = self.llm.generate_answer(query, results)

            print(f"\n🤖: {answer}\n")


# ---------------- RUN ----------------

if __name__ == "__main__":


    analyzer = AgreementAnalyzer()

    file_path = input("Enter file path: ")

    analyzer.process_file(file_path)  # use file_path as file_name for simplicity   
    print("\n[ALL CHUNKS]\n")
    
    summary = analyzer.generate_summary()

    
    print("\n📄 SUMMARY:\n")
    print(summary)

    analyzer.chat()