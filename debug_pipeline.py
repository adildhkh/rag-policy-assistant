"""
RAG Pipeline Debugger - Test each component step by step
Run this from your project root directory
"""

import sys
from pathlib import Path
import os

# Add src to path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(step_num, title):
    """Print step header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}STEP {step_num}: {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_info(msg):
    """Print info message"""
    print(f"  {msg}")

# =============================================================================
# STEP 1: Check Environment and API Key
# =============================================================================
def step1_check_environment():
    """Check if environment is set up correctly"""
    print_step(1, "Environment Check")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print_success(f"OPENAI_API_KEY found (length: {len(api_key)})")
        print_info(f"Key preview: {api_key[:7]}...{api_key[-4:]}")
    else:
        print_error("OPENAI_API_KEY not found in environment!")
        print_info("Make sure .env file exists with: OPENAI_API_KEY=sk-...")
        return False
    
    # Check project structure
    print_info("\nChecking project structure...")
    required_paths = [
        ("src directory", Path("src")),
        ("data directory", Path("data")),
        ("policies directory", Path("data/policies")),
    ]
    
    all_exist = True
    for name, path in required_paths:
        if path.exists():
            print_success(f"{name} exists: {path}")
        else:
            print_error(f"{name} NOT found: {path}")
            all_exist = False
    
    return all_exist

# =============================================================================
# STEP 2: Check Policy Files
# =============================================================================
def step2_check_files():
    """Check if policy files exist and are readable"""
    print_step(2, "Policy Files Check")
    
    policies_dir = Path("data/policies")
    
    if not policies_dir.exists():
        print_error(f"Policies directory not found: {policies_dir}")
        return False
    
    # Find all text files (.txt and .md)
    txt_files = list(policies_dir.glob("*.txt"))
    md_files = list(policies_dir.glob("*.md"))
    policy_files = txt_files + md_files
    
    print_info(f"Searching in: {policies_dir.absolute()}")
    print_info(f"Found {len(txt_files)} .txt files")
    print_info(f"Found {len(md_files)} .md files")
    print_info(f"Total: {len(policy_files)} policy files\n")
    
    if not policy_files:
        print_error("No .txt or .md files found in policies directory!")
        print_info("Expected files like: pto_policy.txt, remote_work.md, etc.")
        return False
    
    total_size = 0
    for file in policy_files:
        size = file.stat().st_size
        total_size += size
        print_success(f"{file.name:<30} ({size:,} bytes)")
        
        # Read first 100 chars to verify
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read(100)
                print_info(f"  Preview: {content[:80]}...")
        except Exception as e:
            print_error(f"  Error reading file: {e}")
            return False
    
    print_info(f"\nTotal data: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    return True

# =============================================================================
# STEP 3: Test Document Processing
# =============================================================================
def step3_test_processing():
    """Test document processing and chunking"""
    print_step(3, "Document Processing Test")
    
    try:
        from src.document_processor import process_policies
        print_success("Imported process_policies function")
    except ImportError as e:
        print_error(f"Cannot import process_policies: {e}")
        return None
    
    policies_dir = Path("data/policies")
    
    print_info(f"Processing documents from: {policies_dir}")
    print_info("This may take a moment...")
    
    try:
        chunks = process_policies(str(policies_dir))
        print_success(f"Created {len(chunks)} document chunks")
        
        if chunks:
            print_info("\nSample chunk:")
            print_info(f"  Content: {chunks[0].page_content[:150]}...")
            print_info(f"  Metadata: {chunks[0].metadata}")
            
            # Analyze chunks
            print_info("\nChunk analysis:")
            total_chars = sum(len(c.page_content) for c in chunks)
            avg_chars = total_chars / len(chunks)
            print_info(f"  Total characters: {total_chars:,}")
            print_info(f"  Average chunk size: {avg_chars:.0f} characters")
            
            # Count by source
            sources = {}
            for chunk in chunks:
                source = chunk.metadata.get('source', 'unknown')
                sources[source] = sources.get(source, 0) + 1
            
            print_info(f"\n  Chunks per file:")
            for source, count in sorted(sources.items()):
                print_info(f"    {Path(source).name}: {count} chunks")
        else:
            print_error("No chunks created!")
        
        return chunks
    
    except Exception as e:
        print_error(f"Error processing documents: {e}")
        import traceback
        print(traceback.format_exc())
        return None

# =============================================================================
# STEP 4: Test Vector Store Creation
# =============================================================================
def step4_test_vectorstore(chunks):
    """Test vector store creation"""
    print_step(4, "Vector Store Creation Test")
    
    if not chunks:
        print_error("No chunks provided - skipping vector store test")
        return None
    
    try:
        from src.vector_store import get_or_create_vector_store
        print_success("Imported get_or_create_vector_store function")
    except ImportError as e:
        print_error(f"Cannot import vector store function: {e}")
        return None
    
    # Use a test directory
    test_persist_dir = Path("test_chroma_db")
    
    print_info(f"Creating vector store with {len(chunks)} chunks")
    print_info(f"Persist directory: {test_persist_dir.absolute()}")
    print_info("This will call OpenAI embeddings API...")
    
    try:
        vectorstore = get_or_create_vector_store(
            chunks=chunks,
            persist_directory=str(test_persist_dir)
        )
        print_success("Vector store created successfully!")
        
        # Test retrieval
        print_info("\nTesting retrieval...")
        test_query = "vacation days"
        results = vectorstore.similarity_search(test_query, k=3)
        
        print_success(f"Retrieved {len(results)} results for query: '{test_query}'")
        if results:
            print_info("\nTop result:")
            print_info(f"  Content: {results[0].page_content[:200]}...")
            print_info(f"  Source: {results[0].metadata.get('source', 'N/A')}")
        
        return vectorstore
    
    except Exception as e:
        print_error(f"Error creating vector store: {e}")
        import traceback
        print(traceback.format_exc())
        return None

# =============================================================================
# STEP 5: Test RAG Pipeline
# =============================================================================
def step5_test_rag(vectorstore):
    """Test the complete RAG pipeline"""
    print_step(5, "RAG Pipeline Test")
    
    if not vectorstore:
        print_error("No vector store provided - skipping RAG test")
        return False
    
    try:
        from src.rag_pipeline import rag_answer
        print_success("Imported rag_answer function")
    except ImportError as e:
        print_error(f"Cannot import rag_answer: {e}")
        return False
    
    test_questions = [
        "How many vacation days do employees get?",
        "What is the remote work policy?",
        "What are the password requirements?"
    ]
    
    print_info(f"Testing with {len(test_questions)} questions...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{Colors.BOLD}Question {i}:{Colors.RESET} {question}")
        
        try:
            result = rag_answer(vectorstore, question, k=3)
            
            print_success("Got answer!")
            print_info(f"  Answer: {result['answer'][:200]}...")
            print_info(f"  Sources: {len(result['sources'])} documents")
            
            if result['sources']:
                print_info(f"  First source: {result['sources'][0].get('file', 'N/A')}")
        
        except Exception as e:
            print_error(f"Error answering question: {e}")
            import traceback
            print(traceback.format_exc())
            return False
    
    return True

# =============================================================================
# STEP 6: Check Existing Vector Store
# =============================================================================
def step6_check_existing_vectorstore():
    """Check if existing vector store has data"""
    print_step(6, "Check Existing Vector Store (chroma_db)")
    
    persist_dir = Path("chroma_db")
    
    if not persist_dir.exists():
        print_warning(f"No existing vector store found at: {persist_dir}")
        print_info("This is okay - it will be created on first run")
        return None
    
    print_info(f"Found existing vector store at: {persist_dir.absolute()}")
    
    # Check directory contents
    files = list(persist_dir.rglob("*"))
    print_info(f"Contains {len(files)} files/folders")
    
    try:
        from src.vector_store import get_or_create_vector_store
        
        print_info("Loading existing vector store...")
        vectorstore = get_or_create_vector_store(
            persist_directory=str(persist_dir)
        )
        
        # Try to get collection info
        try:
            # Test a simple search
            results = vectorstore.similarity_search("test", k=1)
            print_success(f"Vector store is functional")
            print_info(f"Retrieved {len(results)} results from test query")
            
            if results:
                print_success("Vector store contains data!")
                return vectorstore
            else:
                print_warning("Vector store is empty (0 results)")
                return None
        except Exception as e:
            print_error(f"Error querying vector store: {e}")
            return None
    
    except Exception as e:
        print_error(f"Error loading vector store: {e}")
        import traceback
        print(traceback.format_exc())
        return None

# =============================================================================
# MAIN DEBUG SEQUENCE
# =============================================================================
def main():
    """Run all debug steps"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       RAG PIPELINE DEBUGGER - Insha Allah                 ║")
    print("║       Testing Policy Assistant Components                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    # Step 1: Environment
    if not step1_check_environment():
        print_error("\n❌ Environment check failed. Fix issues above and try again.")
        return
    
    # Step 2: Files
    if not step2_check_files():
        print_error("\n❌ File check failed. Make sure policy files exist.")
        return
    
    # Step 3: Processing
    chunks = step3_test_processing()
    if not chunks:
        print_error("\n❌ Document processing failed. Check error above.")
        return
    
    # Step 4: Vector Store
    vectorstore = step4_test_vectorstore(chunks)
    if not vectorstore:
        print_error("\n❌ Vector store creation failed. Check error above.")
        return
    
    # Step 5: RAG
    if not step5_test_rag(vectorstore):
        print_error("\n❌ RAG pipeline test failed. Check error above.")
        return
    
    # Step 6: Check production vector store
    step6_check_existing_vectorstore()
    
    # Final summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                  ✅ ALL TESTS PASSED! ✅                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    print_success("Your RAG pipeline is working correctly!")
    print_info("\nNext steps:")
    print_info("1. If you see 0 chunks in Streamlit, delete chroma_db folder")
    print_info("2. Click 'Initialize System' in Streamlit")
    print_info("3. The system should now load your documents")
    
    print(f"\n{Colors.YELLOW}Note: Test vector store created at: test_chroma_db{Colors.RESET}")
    print_info("You can delete this folder after testing")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nDebug interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        import traceback
        print(traceback.format_exc())