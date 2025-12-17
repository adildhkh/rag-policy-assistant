"""
RAG Policy Assistant - Streamlit Web Application
Company policy question answering with RAG
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import hashlib

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
    page_title="Policy Assistant",
    page_icon="📚",
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
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
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

if 'collection_version' not in st.session_state:
    st.session_state.collection_version = 1


def get_policies_hash():
    """
    Calculate hash of all policy files to detect changes
    """
    policies_dir = Path(__file__).parent.parent / "data" / "policies"
    
    if not policies_dir.exists():
        return None
    
    # Get all markdown files
    md_files = sorted(policies_dir.glob("*.md"))
    
    # Create hash from file contents
    hasher = hashlib.md5()
    for md_file in md_files:
        with open(md_file, 'rb') as f:
            hasher.update(f.read())
    
    return hasher.hexdigest()


def initialize_vectorstore(force_reload=False):
    """
    Initialize or load vector store
    
    Args:
        force_reload: If True, recreate even if exists
    """
    with st.spinner("🔄 Initializing system..."):
        try:
            policies_dir = Path(__file__).parent.parent / "data" / "policies"
            persist_dir = Path(__file__).parent.parent / "chroma_db"
            
            # Get current policies hash
            current_hash = get_policies_hash()
            
            # Check if we need to reload
            need_reload = force_reload
            
            if persist_dir.exists() and not force_reload:
                # Check if policies have changed
                hash_file = persist_dir / ".policies_hash"
                if hash_file.exists():
                    with open(hash_file, 'r') as f:
                        stored_hash = f.read().strip()
                    if stored_hash != current_hash:
                        st.info("📝 Policy changes detected. Reloading...")
                        need_reload = True
                else:
                    # No hash file, assume first run
                    need_reload = False
            else:
                need_reload = True
            
            # Close existing connection if reloading
            if need_reload and st.session_state.vectorstore is not None:
                try:
                    # Close connection gracefully
                    st.session_state.vectorstore._client.reset()
                except:
                    pass
                st.session_state.vectorstore = None
                
                # Force garbage collection
                import gc
                gc.collect()
                
                # Small delay
                import time
                time.sleep(0.5)
            
            # Create or load vector store
            if need_reload:
                # Process policies
                chunks = process_policies(str(policies_dir))
                
                # Use versioned collection name to avoid conflicts
                collection_name = f"policy_documents_v{st.session_state.collection_version}"
                
                # Create new vector store with force_recreate
                vectorstore = get_or_create_vector_store(
                    chunks=chunks,
                    persist_directory=str(persist_dir),
                    collection_name=collection_name,
                    force_recreate=True
                )
                
                # Save hash
                hash_file = persist_dir / ".policies_hash"
                with open(hash_file, 'w') as f:
                    f.write(current_hash)
                
                if force_reload:
                    st.success("✅ Policies reloaded successfully!")
                else:
                    st.success("✅ System ready! Ask me anything about company policies.")
            else:
                # Load existing
                collection_name = f"policy_documents_v{st.session_state.collection_version}"
                vectorstore = get_or_create_vector_store(
                    persist_directory=str(persist_dir),
                    collection_name=collection_name
                )
                st.success("✅ System ready! Ask me anything about company policies.")
            
            # Update session state
            st.session_state.vectorstore = vectorstore
            st.session_state.vectorstore_loaded = True
            
        except Exception as e:
            st.error(f"❌ Error initializing system: {str(e)}")
            st.session_state.vectorstore_loaded = False


def reload_policies():
    """
    Reload policies - production ready solution
    Works on all operating systems including Windows
    """
    try:
        with st.spinner("♻️ Reloading policies..."):
            # Increment collection version to use new collection
            st.session_state.collection_version += 1
            
            # Reinitialize with force reload
            initialize_vectorstore(force_reload=True)
            
            return True
            
    except Exception as e:
        st.error(f"❌ Error reloading policies: {str(e)}")
        return False


def show_health_check():
    """Display health check status"""
    st.markdown("## 🏥 System Health Check")
    st.markdown("---")
    
    try:
        # Get health status
        health_data = check_system_health(st.session_state.vectorstore)
        
        # Overall status
        status = health_data.get("status", "unknown")
        if status == "healthy":
            st.success("✅ System Status: HEALTHY")
        elif status == "degraded":
            st.warning("⚠️ System Status: DEGRADED")
        else:
            st.error("❌ System Status: UNHEALTHY")
        
        st.markdown("---")
        
        # Component status
        st.markdown("### Component Status")
        
        components = health_data.get("components", {})
        
        # OpenAI API
        api_status = components.get("openai_api", "unknown")
        if api_status == "configured":
            st.success("✅ OpenAI API: Configured")
        else:
            st.error("❌ OpenAI API: Not configured")
        
        # Vector Store
        vs_data = components.get("vector_store", {})
        if isinstance(vs_data, dict):
            vs_status = vs_data.get("status", "unknown")
            if vs_status == "loaded":
                chunks = vs_data.get("chunks", 0)
                st.success(f"✅ Vector Store: Loaded ({chunks} chunks)")
            else:
                st.warning(f"⚠️ Vector Store: {vs_status}")
        else:
            st.warning(f"⚠️ Vector Store: {vs_data}")
        
        st.markdown("---")
        
        # Additional info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Policy Documents", "8")
        
        with col2:
            if isinstance(vs_data, dict):
                st.metric("Vector Chunks", vs_data.get("chunks", 0))
            else:
                st.metric("Vector Chunks", "N/A")
        
        with col3:
            st.metric("Streamlit Version", st.__version__)
        
        st.markdown("---")
        
        # JSON output
        with st.expander("📊 View Raw Health Data (JSON)"):
            # Add timestamp
            health_data["timestamp"] = datetime.now().isoformat()
            health_data["policies_loaded"] = 8
            health_data["streamlit_version"] = st.__version__
            health_data["collection_version"] = st.session_state.collection_version
            
            st.json(health_data)
        
        st.markdown("---")
        st.info("💡 This health check endpoint verifies all system components are functioning correctly.")
        
    except Exception as e:
        st.error(f"❌ Error checking system health: {str(e)}")
        st.json({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })


def main():
    """Main application"""
    
    # Check for health check query parameter
    query_params = st.query_params
    if "health" in query_params or "healthcheck" in query_params:
        show_health_check()
        st.markdown("---")
        if st.button("← Back to Chat Interface"):
            # Clear query params and rerun
            st.query_params.clear()
            st.rerun()
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📚 Policy Assistant")
        st.markdown("---")
        
        # API Key check
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.error("❌ OPENAI_API_KEY not found")
            st.info("Set your API key in Streamlit secrets")
        
        st.markdown("---")
        
        # System status
        st.markdown("### System Status")
        if st.session_state.vectorstore_loaded:
            st.success("🟢 Ready")
            st.info("📚 8 policy documents loaded")
        else:
            st.warning("🟡 Not initialized")
        
        st.markdown("---")
        
        # Initialize button
        if st.button("🔄 Initialize System", use_container_width=True):
            initialize_vectorstore()
            st.rerun()
        
        # Reload button - PRODUCTION READY
        if st.button("♻️ Reload Policies", use_container_width=True):
            if reload_policies():
                st.rerun()
        
        with st.expander("ℹ️ About Reloading"):
            st.markdown("""
            **When to reload:**
            - After updating policy documents
            - To refresh with latest content
            
            **How it works:**
            - Automatically detects policy changes
            - Creates new vector database
            - Works on all operating systems
            - No manual deletion needed ✅
            """)
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Health Check button
        if st.button("🏥 Health Check", use_container_width=True):
            st.query_params["health"] = "true"
            st.rerun()
        
        st.markdown("---")
        
        # Info
        st.markdown("### About")
        st.markdown("""
        This AI assistant answers questions about company policies using:
        - **RAG** (Retrieval-Augmented Generation)
        - **OpenAI GPT-3.5-turbo**
        - **ChromaDB** vector store
        
        **Coverage:**
        - PTO & Leave
        - Remote Work
        - Information Security
        - Expenses
        - Training
        - Benefits
        - Ethics
        - Data Privacy
        """)
    
    # Main content
    st.markdown('<div class="main-header">📚 Company Policy Assistant</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask me anything about our company policies</div>', 
                unsafe_allow_html=True)
    
    # Check if system is ready
    if not st.session_state.vectorstore_loaded:
        st.warning("⚠️ System not initialized. Click 'Initialize System' in the sidebar.")
        
        # Auto-initialize on first run
        if st.button("🚀 Get Started"):
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
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = rag_answer(
                        st.session_state.vectorstore,
                        prompt,
                        k=4
                    )
                    
                    answer = result["answer"]
                    sources = result["sources"]
                    
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
                    st.error(error_msg)
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
        
        **For Streamlit Cloud:**
        Add your API key in the Secrets management section
        
        **For local development:**
        Create a .env file with:
        ```
        OPENAI_API_KEY=sk-your-api-key-here
        ```
        
        Then restart the app.
        """)
        st.stop()
    
    main()