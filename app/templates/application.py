import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.components.data_loader import process_and_store_pdfs
from app.components.retriever import create_qa_chain
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def main():
    st.set_page_config(page_title="AgenticRAG", page_icon="🤖")
    st.title("🤖 Agentic RAG System")
    st.markdown("Upload PDFs and ask questions using advanced RAG capabilities")
    
    # Sidebar for PDF processing
    with st.sidebar:
        st.header("📁 Document Processing")
        if st.button("Process PDFs"):
            with st.spinner("Processing PDFs and creating vector store..."):
                try:
                    process_and_store_pdfs()
                    st.success("✅ PDFs processed successfully!")
                except Exception as e:
                    st.error(f"❌ Error processing PDFs: {str(e)}")
    
    # Main chat interface
    st.header("💬 Ask Questions")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    qa_chain = create_qa_chain()
                    result = qa_chain.invoke({"query": prompt})
                    response = result["result"]
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
