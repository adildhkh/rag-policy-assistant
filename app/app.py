"""
RAG Policy Assistant - Streamlit Web Application
Company policy question answering with RAG
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json

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


def initialize_vectorstore():
    """Initialize or load vector store"""
    with st.spinner("🔄 Loading policy documents..."):
        try:
            policies_dir = Path(__file__).parent.parent / "data" / "policies"
            persist_dir = Path(__file__).parent.parent / "chroma_db"
            
            # Check if vector store exists
            if persist_dir.exists():
                st.info("📂 Loading existing vector store...")
                vectorstore = get_or_create_vector_store(
                    persist_directory=str(persist_dir)
                )
            else:
                st.info("📄 Processing policy documents...")
                chunks = process_policies(str(policies_dir))
                st.success(f"✅ Created {len(chunks)} document chunks")
                
                st.info("🔢 Generating embeddings...")
                vectorstore = get_or_create_vector_store(
                    chunks=chunks,
                    persist_directory=str(persist_dir)
                )
            
            st.session_state.vectorstore = vectorstore
            st.session_state.vectorstore_loaded = True
            st.success("✅ System ready!")
            
        except Exception as e:
            st.error(f"❌ Error initializing system: {str(e)}")
            st.session_state.vectorstore_loaded = False


def main():
    """Main application"""
    
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
            st.info("Set your API key in .env file")
        
        st.markdown("---")
        
        # System status
        st.markdown("### System Status")
        if st.session_state.vectorstore_loaded:
            st.success("🟢 Ready")
            
            # Show health info
            health = check_system_health(st.session_state.vectorstore)
            
            # Safe handling of vector store status
            vs_info = health["components"]["vector_store"]
            if isinstance(vs_info, dict):
                chunks = vs_info.get("chunks", 0)
            else:
                chunks = 0  # Not loaded yet
            
            st.metric("Documents Indexed", f"{chunks} chunks")
        else:
            st.warning("🟡 Not initialized")
        
        st.markdown("---")
        
        # Initialize button
        if st.button("🔄 Initialize System", use_container_width=True):
            initialize_vectorstore()
        
        # Reload button
        if st.button("♻️ Reload Policies", use_container_width=True):
            with st.spinner("Reloading..."):
                persist_dir = Path(__file__).parent.parent / "chroma_db"
                if persist_dir.exists():
                    import shutil
                    shutil.rmtree(persist_dir)
                st.session_state.vectorstore = None
                st.session_state.vectorstore_loaded = False
                initialize_vectorstore()
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
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


# Health check endpoint (for deployment)
def health_check():
    """Health check for monitoring"""
    health = check_system_health(st.session_state.vectorstore)
    return health


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