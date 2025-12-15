# RAG Policy Assistant

A production‑ready Retrieval‑Augmented Generation (RAG) system that answers questions strictly within the scope of company policy documents.

---

## 📋 Project Overview

**RAG Policy Assistant** is designed for HR, compliance, and internal knowledge use‑cases where factual accuracy and grounding are critical.

The system:

* Ingests Markdown‑based policy documents
* Chunks and embeds them into a vector database
* Retrieves relevant context per query
* Generates grounded answers using an LLM
* Supports evaluation and debugging workflows

---

## 🏗️ Architecture

```
Documents → Chunking → Embeddings → Vector Store → Retrieval → LLM → Answer
```

### Tech Stack

* **LLM**: OpenAI (GPT‑4 / GPT‑3.5)
* **Embeddings**: `text-embedding-3-small`
* **Vector Store**: ChromaDB
* **Backend**: Python
* **UI**: Streamlit
* **CI/CD**: GitHub Actions

---

## 📦 Installation

### Prerequisites

* Python 3.9+
* OpenAI API key

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/rag-policy-assistant.git
cd rag-policy-assistant
```

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app/app.py
```

---

## 📂 Project Structure

```
rag-policy-assistant/
├── app/
│   ├── app.py                # Streamlit application
│   └── app_debug.py          # Debug mode
├── data/
│   └── policies/             # Policy documents (Markdown)
├── evaluation/
│   └── evaluation_results.json
├── src/
│   ├── document_processor.py # Document loading & chunking
│   ├── vector_store.py       # Vector DB logic
│   └── rag_pipeline.py       # Core RAG pipeline
├── .github/
│   └── workflows/
│       └── ci.yml            # CI pipeline
├── design-and-evaluation.md
├── ai-tooling.md
├── deployed.md
├── requirements.txt
├── .env.example
├── .gitignore
├── show_project_structure.py
├── test_system.py
└── README.md
```

---

## 🎯 Features

* Policy‑scoped question answering
* Source‑grounded responses
* Semantic search over documents
* Streamlit chat interface
* Debug and evaluation support
* CI pipeline validation

---

## 📊 Evaluation

Evaluation results are stored in:

```
evaluation/evaluation_results.json
```

Metrics include groundedness, relevance, hallucination rate, and latency.

---

## 🚀 Deployment

Deployment instructions and notes are provided in `deployed.md`.

Supported platforms:

* Streamlit Cloud
* Render
* Railway
* Heroku

---

## 🤖 AI Tooling

See `ai-tooling.md` for details on AI‑assisted development tools used.

---

## 👤 Author

**Adil Naseer Khawaja**

---

## 📝 License

Educational / demonstration use.
