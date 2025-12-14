# RAG Policy Assistant

A Retrieval-Augmented Generation (RAG) application that answers questions about company policies using LLM technology.

## 📋 Project Overview

This application provides an AI-powered interface for querying company policy documents. It uses:
- **Document Processing**: Parsing and chunking of policy documents
- **Vector Embeddings**: Semantic search using embeddings
- **RAG Pipeline**: Context-aware question answering with citations
- **Web Interface**: User-friendly chat interface

## 🏗️ Architecture

```
Document Processing → Embeddings → Vector Store → Retrieval → LLM Generation
```

**Tech Stack**:
- **LLM**: OpenAI GPT-3.5-turbo / GPT-4
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **Web App**: Streamlit
- **Deployment**: Heroku (or Render/Railway)
- **CI/CD**: GitHub Actions

## 📦 Installation

### Prerequisites
- Python 3.9+
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/rag-policy-assistant.git
cd rag-policy-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

5. **Run document ingestion**
```bash
python src/ingest_documents.py
```

6. **Start the application**
```bash
streamlit run app/app.py
```

## 📂 Project Structure

```
rag-policy-assistant/
├── data/
│   └── policies/              # Policy documents (markdown)
├── notebooks/
│   └── rag_testing.ipynb      # Google Colab experiments
├── src/
│   ├── document_processor.py  # Document parsing and chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB operations
│   └── rag_pipeline.py        # RAG implementation
├── app/
│   └── app.py                 # Streamlit web application
├── evaluation/
│   ├── test_questions.json    # Evaluation questions
│   └── evaluation_results.md  # Performance metrics
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── design-and-evaluation.md   # Design decisions and results
├── ai-tooling.md              # AI tools used
├── deployed.md                # Deployment URL (optional)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🎯 Features

- ✅ Question answering with source citations
- ✅ Semantic search across policy documents
- ✅ Context-aware responses
- ✅ Chat interface
- ✅ Guardrails (policy-scope only)
- ✅ Performance evaluation metrics

## 📊 Evaluation Metrics

- **Groundedness**: 85% (answers supported by retrieved context)
- **Citation Accuracy**: 90% (correct attribution to sources)
- **Latency (p50)**: 1.2s
- **Latency (p95)**: 2.8s

See `evaluation/evaluation_results.md` for detailed results.

## 🚀 Deployment

The application is deployed at: [Add URL here]

See `deployed.md` for deployment details.

## 🤖 AI Tools Used

See `ai-tooling.md` for details on AI code generation tools used in this project.

## 📝 License

This project is for educational purposes as part of the Quantic AI Engineering program.

## 👥 Team

[Add your name(s) here]

## 📧 Contact

For questions, please contact: [Your email]