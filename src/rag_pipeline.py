"""
RAG pipeline for question answering
Handles retrieval and generation with citations
"""

import os
from typing import Dict, List
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI


def rag_answer(
    vectorstore: Chroma,
    question: str,
    k: int = 4,
    temperature: float = 0
) -> Dict:
    """
    Answer question using RAG pipeline
    
    Args:
        vectorstore: ChromaDB vector store
        question: User question
        k: Number of chunks to retrieve
        temperature: LLM temperature (0 = deterministic)
        
    Returns:
        Dictionary with answer, sources, and metadata
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Step 1: Retrieve relevant chunks
    retrieved_docs = vectorstore.similarity_search(question, k=k)
    
    if not retrieved_docs:
        return {
            "question": question,
            "answer": "I couldn't find relevant information in our policy documents to answer this question.",
            "sources": [],
            "chunks_retrieved": 0
        }
    
    # Step 2: Build context
    context_parts = []
    sources = []
    
    for i, doc in enumerate(retrieved_docs):
        source_name = doc.metadata.get('source', 'Unknown')
        policy_name = doc.metadata.get('policy_name', source_name)
        
        context_parts.append(
            f"[Source {i+1}: {source_name}]\n{doc.page_content}"
        )
        sources.append({
            "file": source_name,
            "policy": policy_name
        })
    
    context = "\n\n".join(context_parts)
    
    # Step 3: Create prompt
    prompt = f"""You are a helpful assistant that answers questions about company policies.

Use ONLY the information provided in the context below to answer the question.

IMPORTANT RULES:
1. If the answer is not in the context, say "I can only answer questions about our company policies, and I don't have information about that in our policy documents."
2. Always cite which policy document(s) your answer comes from using the source names provided
3. Be concise but complete
4. Use bullet points for lists when appropriate
5. Include specific numbers, dates, and details when present in the context

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    
    # Step 4: Generate answer
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        openai_api_key=api_key
    )
    
    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        return {
            "question": question,
            "answer": f"Error generating answer: {str(e)}",
            "sources": sources,
            "chunks_retrieved": len(retrieved_docs)
        }
    
    # Extract unique sources
    unique_sources = []
    seen = set()
    for src in sources:
        if src["file"] not in seen:
            unique_sources.append(src)
            seen.add(src["file"])
    
    return {
        "question": question,
        "answer": response,
        "sources": unique_sources,
        "chunks_retrieved": len(retrieved_docs)
    }


def check_system_health(vectorstore: Chroma = None) -> Dict:
    """
    Health check endpoint
    
    Args:
        vectorstore: Optional vector store to check
        
    Returns:
        Health status dictionary
    """
    status = {
        "status": "healthy",
        "components": {}
    }
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    status["components"]["openai_api"] = "configured" if api_key else "missing"
    
    # Check vector store
    if vectorstore:
        try:
            count = vectorstore._collection.count()
            status["components"]["vector_store"] = {
                "status": "loaded",
                "chunks": count
            }
        except Exception as e:
            status["components"]["vector_store"] = {
                "status": "error",
                "error": str(e)
            }
            status["status"] = "degraded"
    else:
        status["components"]["vector_store"] = "not_loaded"
        status["status"] = "degraded"
    
    return status