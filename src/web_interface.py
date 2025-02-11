import streamlit as st
import asyncio
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from rag_qa_system import RAGQuestionAnswerer
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_system():
    
    if 'rag_system' not in st.session_state:
        vector_store = VectorStoreManager()
        st.session_state.rag_system = RAGQuestionAnswerer(vector_store)

def main():
    st.title("AskMate")
    
    # Initialize system
    initialize_system()
    
    # File upload section
    st.sidebar.header("📄 Document Upload")
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF documents", 
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.sidebar.button("Process Documents"):
            with st.spinner("Processing documents..."):
                # Save uploaded files temporarily
                if not os.path.exists('temp_docs'):
                    os.makedirs('temp_docs')
                
                for file in uploaded_files:
                    with open(f'temp_docs/{file.name}', 'wb') as f:
                        f.write(file.getbuffer())
                
                # Process documents
                processor = DocumentProcessor()
                documents = processor.load_pdfs('./temp_docs')
                
                # Update vector store
                st.session_state.rag_system.vector_store.create_collection()
                st.session_state.rag_system.vector_store.upsert_documents(documents)
                
                st.sidebar.success(f"Processed {len(documents)} document chunks!")
    
    # Q&A section
    st.header("Question Block:")
    user_question = st.text_input("What would you like to know about your document?")
    
    if user_question:
        with st.spinner("Generating answer..."):
            # Get answer
            answer = asyncio.run(st.session_state.rag_system.answer_question(user_question))
            
            # Display answer
            st.markdown("### Answer:")
            st.write(answer)
            
            # Display sources
            st.markdown("### Sources:")
            sources = st.session_state.rag_system.get_sources(user_question)
            for i, source in enumerate(sources, 1):
                with st.expander(f"Source {i} - {source['metadata']['source']} (Page {source['metadata']['page']})"):
                    st.write(source['content'])

if __name__ == "__main__":
    main()