from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import uuid
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

class VectorStoreManager:
    def __init__(self, collection_name: str = 'document_collection'):
        
        if os.getenv('QDRANT_URL') and os.getenv('QDRANT_API_KEY'):
            self.client = QdrantClient(
                url=os.getenv('QDRANT_URL'),
                api_key=os.getenv('QDRANT_API_KEY')
            )
        else:
            
            self.client = QdrantClient(
                host=os.getenv('QDRANT_HOST', 'localhost'),
                port=int(os.getenv('QDRANT_PORT', 6333))
            )
            
        self.collection_name = collection_name
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )
    
    
    def create_collection(self, vector_size: int = 768):  
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"Collection {self.collection_name} created successfully")
        except Exception as e:
            print(f"Collection might already exist: {e}")
    
    def upsert_documents(self, documents: List[dict]):
        points = []
        for doc in documents:
            vector = doc.get('embedding') or self.embeddings.embed_query(doc['content'])
            
            points.append({
                'id': str(uuid.uuid4()),
                'vector': vector,
                'payload': {
                    'content': doc['content'],
                    'metadata': doc['metadata']
                }
            })
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Upserted {len(points)} documents")
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        query_vector = self.embeddings.embed_query(query)
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        return [hit.payload for hit in search_result]