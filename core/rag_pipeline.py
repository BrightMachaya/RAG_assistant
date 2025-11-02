"""
RAG pipeline creation and management
"""
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self):
        self.embeddings = self._get_embeddings()
        
    def _get_embeddings(self):
        """Get embeddings with fallback support"""
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    def _get_llm(self, model_name):
        """Get LLM with fallback support"""
        try:
            from langchain_ollama import OllamaLLM
            return OllamaLLM(
                model=model_name,
                temperature=0.1,
                num_predict=512
            )
        except ImportError:
            from langchain_community.llms import Ollama
            return Ollama(
                model=model_name,
                temperature=0.1,
                num_predict=512
            )
    
    def create_pipeline(self, documents, model_name, folder_path):
        """Create complete RAG pipeline"""
        # Create unique vector store name
        folder_name = os.path.basename(folder_path)
        vector_store_path = f"vector_store_{folder_name.replace(' ', '_')}"
        
        # Load or create vector store
        if os.path.exists(vector_store_path):
            vector_store = FAISS.load_local(vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            
            # Create vector store
            vector_store = FAISS.from_documents(chunks, self.embeddings)
            vector_store.save_local(vector_store_path)
        
        # Create retriever
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create prompt template
        prompt_template = """You are a helpful AI assistant. Use the following context from documents to answer the question accurately and concisely.

Context Information:
{context}

Question: {question}

Please provide a helpful answer based only on the context provided. If the context doesn't contain relevant information, say so clearly.

Answer:"""
        
        QA_PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Get LLM
        llm = self._get_llm(model_name)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": QA_PROMPT},
            return_source_documents=True,
            output_key="result"
        )
        
        return qa_chain
