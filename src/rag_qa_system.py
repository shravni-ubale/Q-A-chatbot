import google.generativeai as genai
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class RAGQuestionAnswerer:
    def __init__(self, 
                 vector_store_manager,
                 top_k_docs: int = 3):
        
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
       
        self.model = genai.GenerativeModel('gemini-pro')
        self.vector_store = vector_store_manager
        self.top_k_docs = top_k_docs
    
    def generate_prompt(self, query: str, context_docs: List[Dict]) -> str:
        
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        prompt = f"""
        Context Information:
        {context}

        Question: {query}

        Instructions:
        - Use only the information provided in the context above to answer the question
        - If the answer cannot be found in the context, say "I cannot find the answer in the provided documents"
        - Provide specific references to the source documents when possible
        - Be concise and direct in your answer

        Answer:
        """
        
        return prompt
    
    async def answer_question(self, query: str) -> str:
       
        try:
            
            context_docs = self.vector_store.search_documents(query, self.top_k_docs)
            
            prompt = self.generate_prompt(query, context_docs)
           
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def get_sources(self, query: str) -> List[Dict]:
        
        return self.vector_store.search_documents(query, self.top_k_docs)