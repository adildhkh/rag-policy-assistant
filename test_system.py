"""
Diagnostic script to test RAG system components
Run this to check if everything is working
"""

import os
import sys
from pathlib import Path

# Load environment
from dotenv import load_dotenv
load_dotenv()

print("="*70)
print("RAG SYSTEM DIAGNOSTICS")
print("="*70)

# Test 1: Check API Key
print("\n1️⃣ Checking API Key...")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"   ✅ API Key found: {api_key[:20]}...")
else:
    print("   ❌ API Key NOT found!")
    sys.exit(1)

# Test 2: Check Policy Files
print("\n2️⃣ Checking Policy Files...")
policies_dir = Path("data/policies")
if not policies_dir.exists():
    print(f"   ❌ Directory not found: {policies_dir}")
    sys.exit(1)

md_files = list(policies_dir.glob("*.md"))
print(f"   ✅ Found {len(md_files)} policy files:")
for f in md_files:
    size = f.stat().st_size
    print(f"      - {f.name} ({size:,} bytes)")

if len(md_files) == 0:
    print("   ❌ No .md files found!")
    sys.exit(1)

# Test 3: Test Document Loading
print("\n3️⃣ Testing Document Loading...")
try:
    from src.document_processor import load_policy_documents
    docs = load_policy_documents(str(policies_dir))
    print(f"   ✅ Loaded {len(docs)} documents")
    total_chars = sum(len(doc.page_content) for doc in docs)
    print(f"   ✅ Total characters: {total_chars:,}")
except Exception as e:
    print(f"   ❌ Error loading documents: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test Chunking
print("\n4️⃣ Testing Document Chunking...")
try:
    from src.document_processor import chunk_documents
    chunks = chunk_documents(docs, chunk_size=1000, chunk_overlap=200)
    print(f"   ✅ Created {len(chunks)} chunks")
    avg_size = sum(len(c.page_content) for c in chunks) // len(chunks)
    print(f"   ✅ Average chunk size: {avg_size} chars")
except Exception as e:
    print(f"   ❌ Error chunking: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test Embeddings (this might take time)
print("\n5️⃣ Testing Embeddings Generation...")
print("   ⏱️  This will take 20-40 seconds...")
try:
    from langchain_openai import OpenAIEmbeddings
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
    
    # Test with first chunk only
    test_text = chunks[0].page_content[:500]
    print(f"   🧪 Testing with sample text ({len(test_text)} chars)...")
    
    test_embedding = embeddings.embed_query(test_text)
    print(f"   ✅ Generated embedding: {len(test_embedding)} dimensions")
    
except Exception as e:
    print(f"   ❌ Error generating embeddings: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test ChromaDB
print("\n6️⃣ Testing ChromaDB...")
try:
    from langchain_community.vectorstores import Chroma
    
    # Test with just 3 chunks to be fast
    test_chunks = chunks[:3]
    print(f"   🧪 Creating test vector store with {len(test_chunks)} chunks...")
    
    test_vectorstore = Chroma.from_documents(
        documents=test_chunks,
        embedding=embeddings,
        collection_name="test_collection"
    )
    
    # Test search
    results = test_vectorstore.similarity_search("vacation", k=1)
    print(f"   ✅ Vector store created successfully")
    print(f"   ✅ Test search returned {len(results)} results")
    
except Exception as e:
    print(f"   ❌ Error with ChromaDB: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Test Full Pipeline (minimal)
print("\n7️⃣ Testing RAG Pipeline...")
try:
    from src.rag_pipeline import rag_answer
    
    print("   🧪 Testing question answering...")
    result = rag_answer(
        test_vectorstore,
        "How many vacation days?",
        k=2
    )
    
    print(f"   ✅ Generated answer ({len(result['answer'])} chars)")
    print(f"   ✅ Retrieved {result['chunks_retrieved']} chunks")
    print(f"   ✅ Found {len(result['sources'])} sources")
    
except Exception as e:
    print(f"   ❌ Error in RAG pipeline: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 8: Check ChromaDB Directory
print("\n8️⃣ Checking ChromaDB Directory...")
chroma_dir = Path("chroma_db")
if chroma_dir.exists():
    print(f"   ✅ ChromaDB directory exists")
    files = list(chroma_dir.rglob("*"))
    print(f"   ✅ Contains {len(files)} files/folders")
else:
    print(f"   ⚠️  ChromaDB directory doesn't exist yet (will be created)")

# Summary
print("\n" + "="*70)
print("✅ ALL DIAGNOSTICS PASSED!")
print("="*70)
print("\n📊 Summary:")
print(f"   - Policy files: {len(md_files)}")
print(f"   - Documents loaded: {len(docs)}")
print(f"   - Chunks created: {len(chunks)}")
print(f"   - Embeddings: Working ✅")
print(f"   - Vector store: Working ✅")
print(f"   - RAG pipeline: Working ✅")
print("\n🎉 System is ready to use!")
print("\nYou can now run: streamlit run app/app.py")