>/ **An AI-powered Legal Document Intelligence System** — Upload any agreement, extract clauses, get summaries, and ask questions in natural language using RAG.

<br/>

[🚀 Quick Start](#-quick-start) • [📦 Features](#-features) • [🧠 Architecture](#-system-architecture) • [💬 Usage](#-usage) • [🔮 Roadmap](#-roadmap)

</div>

---

## 📌 What Is This?

**Agreement Analyzer AI** is an end-to-end Legal AI pipeline that:

- 🔍 **Extracts & chunks** legal clauses from PDF/DOCX files using Hybrid Semantic Chunking
- 🏷️ **Classifies** clauses by type (Liability, Payment, Termination, etc.)
- 📝 **Summarizes** the entire agreement in structured bullet points
- 💬 **Answers your questions** about the document using RAG (Retrieval-Augmented Generation)
- ⚡ **GPU-accelerated** for fast processing on large documents

No cloud APIs needed. Everything runs **100% locally** using Ollama.

---

## 🚀 Quick Start

### ✅ Prerequisites

Make sure you have the following installed:

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.9+ | [python.org](https://python.org) |
| Git | Latest | [git-scm.com](https://git-scm.com) |
| Ollama | Latest | [ollama.ai](https://ollama.ai) |

---

### 📥 Step 1 — Clone the Repository

```bash
git clone https://github.com/theconquero-r/agreement-analyzer-ai.git
cd agreement-analyzer-ai
```

---

### 📦 Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 **Tip:** Use a virtual environment to avoid conflicts:
> ```bash
> python -m venv venv
> source venv/bin/activate        # Linux/Mac
> venv\Scripts\activate           # Windows
> pip install -r requirements.txt
> ```

---

### 🤖 Step 3 — Setup Ollama (Api Key)

>get a key from ollama.com and past there in the llm.py



**4. Set your model in the config** — open `config.py` (or the top of `main.py`) and set:

```python
OLLAMA_MODEL = "gpt-oss:120b"       # or "mistral", "gemma", etc.
OLLAMA_BASE_URL = "Ollama.com"
```

---

### ▶️ Step 4 — Run the App

**Option A: Web App (Streamlit UI)**

```bash
streamlit run app.py
```

Then open your browser at 👉 `http://localhost:8501`

**Option B: Command Line Interface**

```bash
python main.py
```

Follow the prompts to upload a file and ask questions.

---

## 🎯 Features

<table>
<tr>
<td width="50%">

### 📄 Document Processing
- ✅ PDF support (via PyPDF2)
- ✅ DOCX support (via python-docx)
- ✅ Automatic text extraction & cleaning
- ✅ Sentence-level splitting

</td>
<td width="50%">

### 🧩 Smart Chunking
- ✅ Hybrid Semantic + Keyword Chunking
- ✅ Centroid-based coherence tracking
- ✅ Clause boundary detection
- ✅ Overlap-aware chunking

</td>
</tr>
<tr>
<td width="50%">

### 🏷️ Clause Classification
- ✅ Termination & Liability
- ✅ Payment & Indemnity
- ✅ Confidentiality & Warranty
- ✅ Governing Law & IP/Ownership
- ✅ Dispute Resolution & Delivery

</td>
<td width="50%">

### 💬 AI Q&A (RAG)
- ✅ FAISS vector search
- ✅ Context-grounded answers
- ✅ Hallucination prevention
- ✅ Streamlit chat interface

</td>
</tr>
</table>

---

## 🧠 System Architecture

```
📄 RAW DOCUMENT (PDF / DOCX)
         │
         ▼
   📝 Text Extraction
         │
         ▼
   🧹 Text Cleaning
         │
         ▼
   ✂️  Sentence Splitting (Regex)
         │
         ▼
   🔀 Hybrid Semantic Chunking
      ├── Embedding Similarity (MiniLM)
      └── Keyword-based Clause Detection
         │
         ▼
   🏷️  Clause Classification
         │
         ▼
   🔢 Embedding Generation (all-MiniLM-L6-v2)
         │
         ▼
   📦 FAISS Vector Index
         │
         ▼
   🤖 Ollama LLM  ←──  User Query
         │
         ▼
   💬 RAG-Powered Answer / Summary
```

---

## 💬 Usage

### Web App (Streamlit)

1. Run `streamlit run app.py`
2. Upload your PDF or DOCX legal agreement
3. Wait for automatic analysis (chunking + indexing)
4. Read the AI-generated **summary**
5. Type questions in the **chat box** like:
   - *"What are the payment terms?"*
   - *"When can either party terminate the contract?"*
   - *"What are the liability limitations?"*

### CLI

1. Run `python main.py`
2. Enter the path to your document
3. The system will process and index it
4. Type your question and get an answer

---

## 🗂️ Project Structure

```
agreement-analyzer-ai/
│
├── app.py                  # Streamlit web app
├── main.py                 # CLI entry point
├── requirements.txt        # All dependencies
│
├── chunker.py              # Hybrid chunking logic
├── classifier.py           # Clause type classification
├── embedder.py             # Embedding generation (MiniLM)
├── retriever.py            # FAISS indexing & search
├── llm.py                  # Ollama LLM integration
├── summarizer.py           # Document summarization
│
└── utils/
    ├── extractor.py        # PDF/DOCX text extraction
    └── cleaner.py          # Text cleaning utilities
```

> ⚠️ File structure may slightly vary — refer to actual files in the repo.

---

## ⚙️ Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3` | LLM model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `SIMILARITY_THRESHOLD` | `0.75` | Chunking similarity cutoff |
| `TOP_K_CHUNKS` | `5` | Chunks retrieved per query |
| `CHUNK_OVERLAP` | `1` | Sentence overlap between chunks |

---

## 🔮 Roadmap

- [x] Hybrid Semantic Chunking
- [x] Clause Classification (Rule-based)
- [x] FAISS Vector Search
- [x] RAG Q&A via Ollama
- [x] Streamlit Web UI
- [ ] ⚠️ **Risk Detection Engine** ← *Next Major Feature*
- [ ] ML-Based Clause Classification (Legal-BERT)
- [ ] Header-Aware / Section-Based Chunking
- [ ] Clause-Level Citations & Explainability
- [ ] FastAPI Backend for Production
- [ ] Pinecone / Weaviate Vector DB Support
- [ ] Multi-Document Support

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Web UI | Streamlit |
| Embeddings | Sentence Transformers (MiniLM) |
| Vector Store | FAISS |
| LLM Inference | Ollama (local) |
| Deep Learning | PyTorch |
| PDF Parsing | PyPDF2 |
| DOCX Parsing | python-docx |

---

## 🐛 Troubleshooting

**❌ Ollama connection error?**
```bash
# Make sure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

**❌ CUDA / GPU not detected?**
```bash
# Check PyTorch CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
# If False, the system will automatically fall back to CPU
```

**❌ Model not found?**
```bash
# Pull the model first
ollama pull llama3
```

**❌ Dependency conflicts?**
```bash
# Use a fresh virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/RiskDetection`)
3. Commit your changes (`git commit -m 'Add risk detection engine'`)
4. Push to the branch (`git push origin feature/RiskDetection`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for the Legal AI Community**

⭐ Star this repo if you found it useful!

</div>
