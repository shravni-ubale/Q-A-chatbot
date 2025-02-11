import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
      
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )
    
    def load_pdfs(self, pdf_directory: str) -> List[dict]:
        documents = []
        
        if not os.path.exists(pdf_directory):
            raise ValueError(f"Directory {pdf_directory} does not exist")
        
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_directory, filename)
                loader = PyPDFLoader(pdf_path)
                pdf_documents = loader.load_and_split(self.text_splitter)
                
                for doc in pdf_documents:
                    embedding = self.embeddings.embed_query(doc.page_content)
                    
                    documents.append({
                        'content': doc.page_content,
                        'embedding': embedding,
                        'metadata': {
                            'source': filename,
                            'page': doc.metadata.get('page', 0)
                        }
                    })
        
        return documents

if __name__ == "__main__":
    processor = DocumentProcessor()
    documents = processor.load_pdfs('./documents')
    print(f"Processed {len(documents)} document chunks")