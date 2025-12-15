"""
Document processing module for RAG Policy Assistant
Handles loading and chunking of policy documents
"""

from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_policy_documents(policies_dir: str) -> List[Document]:
    """
    Load all markdown policy files from directory
    
    Args:
        policies_dir: Path to directory containing .md files
        
    Returns:
        List of LangChain Document objects with metadata
    """
    documents = []
    policies_path = Path(policies_dir)
    
    if not policies_path.exists():
        raise FileNotFoundError(f"Policy directory not found: {policies_dir}")
    
    md_files = sorted(policies_path.glob("*.md"))
    
    if not md_files:
        raise ValueError(f"No .md files found in {policies_dir}")
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create Document with metadata
        doc = Document(
            page_content=content,
            metadata={
                "source": md_file.name,
                "policy_name": md_file.stem.replace('-', ' ').title(),
                "file_path": str(md_file)
            }
        )
        documents.append(doc)
    
    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Split documents into chunks for embedding
    
    Args:
        documents: List of documents to chunk
        chunk_size: Target size of each chunk in characters
        chunk_overlap: Overlap between consecutive chunks
        
    Returns:
        List of chunked documents
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks


def process_policies(
    policies_dir: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Complete pipeline: load and chunk policy documents
    
    Args:
        policies_dir: Path to policy directory
        chunk_size: Chunk size in characters
        chunk_overlap: Overlap size in characters
        
    Returns:
        List of chunked documents ready for embedding
    """
    documents = load_policy_documents(policies_dir)
    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    
    return chunks