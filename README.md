# Q&A Chatbot 

Launched site at https://askmate-pdfbot.streamlit.app/

## About the Project

This project demonstrates the integration of modern AI tools to create a functional and intelligent chatbot. It uses:
- **LangChain**: A framework for building language model-based applications.
- **RAG (Retrieval-Augmented Generation)**: Combines retrieval-based and generative models to provide precise and context-aware answers.
- **Qdrant**: A vector search engine used for efficient document retrieval and similarity search.
- **Streamlit**: A user-friendly library for creating interactive web apps.

The chatbot retrieves relevant information from a knowledge base using Qdrant and generates responses using RAG, making it a powerful tool for exploring conversational AI.

---

## Key Features

- **Interactive Chat Interface**: Built with Streamlit, providing a clean and intuitive user interface.
- **RAG Integration**: Combines retrieval and generation for accurate and context-aware responses.
- **Qdrant Vector Search**: Efficiently retrieves relevant documents or information from a knowledge base.
- **Customizable**: Can be extended to integrate with different models (e.g., OpenAI, Google Gemini) or datasets.
- **Real-Time Responses**: Provides instant answers to user queries in a conversational manner.

---

## How It Works

1. The user inputs a question in the chat interface.
2. The chatbot uses **Qdrant** to retrieve the most relevant documents or information from a knowledge base.
3. The retrieved information is passed to the **RAG model**, which generates a context-aware response.
4. The response is displayed to the user in real-time.

---

## Technologies Used

- **Streamlit**: For building the web interface.
- **LangChain**: For natural language processing and question-answering.
- **RAG (Retrieval-Augmented Generation)**: For combining retrieval and generation models.
- **Qdrant**: For efficient vector search and document retrieval.
- **Python**: The core programming language used for development.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/shravni-ubale/Q-A-chatbot.git
   cd Q-A-chatbot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open the app in your browser and start chatting!

---


created by Shravni Ubale
---
