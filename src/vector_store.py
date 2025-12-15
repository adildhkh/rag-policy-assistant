"""
Vector store management for RAG Policy Assistant
Handles ChromaDB operations and embeddings
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def create_vector_store(
    chunks: List[Document],
    persist_directory: str = "./chroma_db",
    collection_name: str = "policy_documents"
) -> Chroma:
    """
    Create and persist ChromaDB vector store with embeddings
    
    Args:
        chunks: List of document chunks
        persist_directory: Directory to save vector store
        collection_name: Name for the collection
        
    Returns:
        ChromaDB vector store
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory
    )
    
    return vectorstore


def load_vector_store(
    persist_directory: str = "./chroma_db",
    collection_name: str = "policy_documents"
) -> Chroma:
    """
    Load existing vector store from disk
    
    Args:
        persist_directory: Directory where vector store is saved
        collection_name: Name of the collection
        
    Returns:
        Loaded ChromaDB vector store
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
    
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    
    return vectorstore


def get_or_create_vector_store(
    chunks: List[Document] = None,
    persist_directory: str = "./chroma_db",
    collection_name: str = "policy_documents",
    force_recreate: bool = False
) -> Chroma:
    """
    Get existing vector store or create new one
    
    Args:
        chunks: Document chunks (required if creating new)
        persist_directory: Directory for vector store
        collection_name: Collection name
        force_recreate: Force recreation even if exists
        
    Returns:
        ChromaDB vector store
    """
    from pathlib import Path
    
    store_path = Path(persist_directory)
    
    # Check if vector store exists
    if store_path.exists() and not force_recreate:
        try:
            return load_vector_store(persist_directory, collection_name)
        except Exception as e:
            print(f"Error loading existing store: {e}")
            print("Creating new vector store...")
    
    # Create new vector store
    if chunks is None:
        raise ValueError("chunks required to create new vector store")
    
    return create_vector_store(chunks, persist_directory, collection_name)