"""
RAG Policy Assistant - Streamlit Web Application (DEBUG VERSION)
Enhanced with detailed error tracking and diagnostics
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
import traceback

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.document_processor import process_policies
from src.vector_store import get_or_create_vector_store
from src.rag_pipeline import rag_answer, check_system_health

# Page config
st.set_page_config(
    page_title="Policy Assistant (DEBUG)",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .debug-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

if 'vectorstore_loaded' not in st.session_state:
    st.session_state.vectorstore_loaded = False

if 'debug_log' not in st.session_state:
    st.session_state.debug_log = []

if 'last_error' not in st.session_state:
    st.session_state.last_error = None


def log_debug(message, level="INFO"):
    """Add message to debug log"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    st.session_state.debug_log.append(log_entry)
    print(log_entry)  # Also print to console


def initialize_vectorstore():
    """Initialize or load vector store with detailed logging"""
    log_debug("Starting vectorstore initialization...")
    
    try:
        policies_dir = Path(__file__).parent.parent / "data" / "policies"
        persist_dir = Path(__file__).parent.parent / "chroma_db"
        
        log_debug(f"Policies dir: {policies_dir}")
        log_debug(f"Persist dir: {persist_dir}")
        log_debug(f"Policies dir exists: {policies_dir.exists()}")
        log_debug(f"Persist dir exists: {persist_dir.exists()}")
        
        # Check if vector store exists
        if persist_dir.exists():
            st.info("📂 Loading existing vector store...")
            log_debug("Loading from existing persist directory")
            
            vectorstore = get_or_create_vector_store(
                persist_directory=str(persist_dir)
            )
            log_debug("Vector store loaded successfully")
            
            # Try to get collection info
            try:
                collection = vectorstore._collection
                count = collection.count()
                log_debug(f"Collection contains {count} vectors")
                st.info(f"✅ Loaded {count} document chunks")
            except Exception as e:
                log_debug(f"Could not get collection count: {e}", "WARN")
            
        else:
            st.info("📄 Processing policy documents...")
            log_debug("No persist directory found, processing documents")
            
            # Check policy files
            if not policies_dir.exists():
                raise FileNotFoundError(f"Policies directory not found: {policies_dir}")
            
            md_files = list(policies_dir.glob("*.md"))
            log_debug(f"Found {len(md_files)} policy files")
            for f in md_files:
                log_debug(f"  - {f.name}")
            
            if len(md_files) == 0:
                raise ValueError("No .md policy files found!")
            
            # Process documents
            chunks = process_policies(str(policies_dir))
            log_debug(f"Created {len(chunks)} chunks")
            st.success(f"✅ Created {len(chunks)} document chunks")
            
            # Create vector store
            st.info("🔢 Generating embeddings...")
            log_debug("Generating embeddings and creating vector store...")
            
            vectorstore = get_or_create_vector_store(
                chunks=chunks,
                persist_directory=str(persist_dir)
            )
            log_debug("Vector store created and persisted")
        
        # Store in session state
        st.session_state.vectorstore = vectorstore
        st.session_state.vectorstore_loaded = True
        st.session_state.last_error = None
        
        log_debug("✅ Initialization complete!")
        st.success("✅ System ready!")
        
        # Test a simple query
        try:
            log_debug("Testing query functionality...")
            test_results = vectorstore.similarity_search("vacation", k=1)
            log_debug(f"Test query returned {len(test_results)} results")
        except Exception as e:
            log_debug(f"Test query failed: {e}", "ERROR")
        
    except Exception as e:
        error_msg = f"Error initializing system: {str(e)}"
        log_debug(error_msg, "ERROR")
        log_debug(f"Traceback: {traceback.format_exc()}", "ERROR")
        
        st.error(f"❌ {error_msg}")
        st.session_state.vectorstore_loaded = False
        st.session_state.last_error = str(e)
        
        # Show detailed error in expander
        with st.expander("🔍 View Error Details"):
            st.code(traceback.format_exc())


def main():
    """Main application"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔍 Policy Assistant (DEBUG)")
        st.markdown("---")
        
        # API Key check
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ API Key configured")
            log_debug("API key found")
        else:
            st.error("❌ OPENAI_API_KEY not found")
            log_debug("API key NOT found", "ERROR")
            st.info("Set your API key in .env file")
        
        st.markdown("---")
        
        # System status
        st.markdown("### System Status")
        if st.session_state.vectorstore_loaded:
            st.success("🟢 Ready")
            
            try:
                # Get health info
                health = check_system_health(st.session_state.vectorstore)
                log_debug(f"Health check result: {health}")
                
                # Safe handling of vector store status
                vs_info = health.get("components", {}).get("vector_store", {})
                
                if isinstance(vs_info, dict):
                    chunks = vs_info.get("chunks", 0)
                    if chunks > 0:
                        st.metric("Documents Indexed", f"{chunks} chunks")
                    else:
                        # Try direct collection count
                        try:
                            count = st.session_state.vectorstore._collection.count()
                            st.metric("Documents Indexed", f"{count} chunks")
                            log_debug(f"Direct count: {count}")
                        except:
                            st.metric("Documents Indexed", "Unknown")
                else:
                    st.metric("Documents Indexed", "Loading...")
                    
            except Exception as e:
                st.warning(f"⚠️ Health check error: {e}")
                log_debug(f"Health check failed: {e}", "ERROR")
        else:
            st.warning("🟡 Not initialized")
            if st.session_state.last_error:
                st.error(f"Last error: {st.session_state.last_error[:100]}...")
        
        st.markdown("---")
        
        # Initialize button
        if st.button("🔄 Initialize System", use_container_width=True):
            st.session_state.debug_log = []  # Clear debug log
            initialize_vectorstore()
            st.rerun()
        
        # Reload button
        if st.button("♻️ Reload Policies", use_container_width=True):
            with st.spinner("Reloading..."):
                persist_dir = Path(__file__).parent.parent / "chroma_db"
                if persist_dir.exists():
                    import shutil
                    log_debug("Removing existing chroma_db directory")
                    shutil.rmtree(persist_dir)
                st.session_state.vectorstore = None
                st.session_state.vectorstore_loaded = False
                st.session_state.debug_log = []
                initialize_vectorstore()
                st.rerun()
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Debug log toggle
        show_debug = st.checkbox("Show Debug Log", value=False)
        
        if show_debug:
            st.markdown("### 🐛 Debug Log")
            if st.button("Clear Log"):
                st.session_state.debug_log = []
                st.rerun()
            
            log_container = st.container()
            with log_container:
                if st.session_state.debug_log:
                    # Show last 20 entries
                    recent_logs = st.session_state.debug_log[-20:]
                    st.text_area(
                        "Recent logs:",
                        value="\n".join(recent_logs),
                        height=300,
                        disabled=True
                    )
                else:
                    st.info("No debug logs yet")
        
        st.markdown("---")
        
        # Info
        st.markdown("### About")
        st.markdown("""
        **Debug Mode Enabled** 🔍
        
        This version includes:
        - Detailed logging
        - Error tracking
        - System diagnostics
        - Better error messages
        """)
    
    # Main content
    st.markdown('<div class="main-header">🔍 Company Policy Assistant (DEBUG)</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask me anything about our company policies</div>', 
                unsafe_allow_html=True)
    
    # Show initialization status
    if not st.session_state.vectorstore_loaded:
        st.warning("⚠️ System not initialized. Click 'Initialize System' in the sidebar.")
        
        # Show last error if exists
        if st.session_state.last_error:
            with st.expander("❌ Last Error Details", expanded=True):
                st.code(st.session_state.last_error)
        
        # Auto-initialize on first run
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("🚀 Get Started", use_container_width=True):
                initialize_vectorstore()
                st.rerun()
        
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("📄 View Sources"):
                        for src in message["sources"]:
                            st.markdown(f"- **{src['policy']}** ({src['file']})")
    
    # Chat input
    if prompt := st.chat_input("Ask about company policies..."):
        log_debug(f"User question: {prompt}")
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    log_debug("Calling RAG pipeline...")
                    result = rag_answer(
                        st.session_state.vectorstore,
                        prompt,
                        k=4
                    )
                    
                    answer = result["answer"]
                    sources = result["sources"]
                    chunks_retrieved = result.get("chunks_retrieved", 0)
                    
                    log_debug(f"Answer generated ({len(answer)} chars)")
                    log_debug(f"Retrieved {chunks_retrieved} chunks")
                    log_debug(f"Found {len(sources)} sources")
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display sources
                    if sources:
                        with st.expander("📄 View Sources"):
                            for src in sources:
                                st.markdown(f"- **{src['policy']}** ({src['file']})")
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    log_debug(f"RAG pipeline error: {error_msg}", "ERROR")
                    log_debug(f"Traceback: {traceback.format_exc()}", "ERROR")
                    
                    st.error(error_msg)
                    
                    with st.expander("🔍 Error Details"):
                        st.code(traceback.format_exc())
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": []
                    })
    
    # Example questions
    if not st.session_state.messages:
        st.markdown("### 💡 Try asking:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - How many vacation days do employees get?
            - What is the remote work policy?
            - What are the password requirements?
            - What's the expense limit for hotels?
            """)
        
        with col2:
            st.markdown("""
            - What is the training budget for engineers?
            - How does the 401k matching work?
            - What's the maternity leave policy?
            - When must security incidents be reported?
            """)


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OPENAI_API_KEY environment variable not set!")
        st.info("""
        Please set your OpenAI API key:
        
        **Option 1: Using .env file (recommended)**
        ```
        OPENAI_API_KEY=sk-your-api-key-here
        ```
        
        **Option 2: Using terminal**
        ```bash
        # Windows PowerShell
        $env:OPENAI_API_KEY="sk-your-api-key-here"
        
        # Mac/Linux
        export OPENAI_API_KEY="sk-your-api-key-here"
        ```
        
        Then restart the app.
        """)
        st.stop()
    
    main()