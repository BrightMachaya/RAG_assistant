#=====Project Name

Bright RAG Assistant with Ollama

#=====Overview

This project is a standalone RAG system with a Tkinter-based GUI that allows you to load .txt documents, 
create embeddings using HuggingFace models, and query them using Ollama LLMs such as llama2, mistral, phi, etc.
It automatically handles.
*Document loading and cleaning
*Chunking and embedding
*Vector storage via FAISS
*Retrieval and LLM-based response generation
*Dynamic model management and live chat interface

## Everything runs locally — no cloud API required once Ollama is installed.

#======Features

*Retrieval-Augmented Generation (RAG) pipeline using LangChain
*Interactive GUI built with Tkinter
*Load .txt documents from any folder
*FAISS vector database for fast semantic retrieval
*HuggingFace embeddings (all-MiniLM-L6-v2)
*Ollama 1.0.1 integration for local LLM inference
*Auto-handling of encoding issues (via chardet)
*Optional sample document creation if folder is empty
*Persistent vector store per document folder

#======Installation

git clone https://github.com/BrightMachaya/RAG_assistant.git

cd RAG_assistant

Install Ollama

run ollama pull e.g, llama2, mistral, phi

#======Run the RAG Assistant
python main.py

Steps in the GUI App
1. Select a Folder containing .txt documents.
2. Choose an Ollama Model (e.g., llama2, mistral, phi).
3. Click “INITIALIZE RAG SYSTEM” — this will:
   Check/install the model (if not available)
   Load and embed documents
   Build or load a FAISS vector store
4. Start asking questions via the chat box!


#======Author
Bright Machaya