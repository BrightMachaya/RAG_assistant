"""
Document processing and RAG system initialization
"""
import os
from .text_loader import RobustTextLoader
from .ollama_manager import OllamaManager
from .rag_pipeline import RAGPipeline

class DocumentProcessor:
    def __init__(self):
        self.ollama_manager = OllamaManager()
        
    def initialize_system(self, folder_path, model_name, status_callback=None):
        """Initialize the complete RAG system"""
        try:
            # Step 1: Check Ollama
            if status_callback:
                status_callback("Checking Ollama service...")
            if not self.ollama_manager.check_ollama_installed():
                raise Exception("Ollama service not running")
            
            # Step 2: Check and download model if needed
            if status_callback:
                status_callback("Checking model availability...")
            if not self.ollama_manager.is_model_available(model_name):
                if status_callback:
                    status_callback(f"Downloading {model_name}... (This may take a while)")
                if not self.ollama_manager.pull_model(model_name):
                    raise Exception(f"Failed to download model: {model_name}")
            
            # Step 3: Load documents
            if status_callback:
                status_callback("Scanning and loading documents...")
            text_files = self.get_all_text_files(folder_path)
            
            if not text_files:
                if status_callback:
                    status_callback("Creating sample document...")
                sample_file = self.create_sample_documents(folder_path)
                text_files = [sample_file]
            
            if status_callback:
                status_callback(f"Processing {len(text_files)} document(s)...")
            
            documents = self.load_documents(text_files)
            
            if not documents:
                raise Exception("No documents could be loaded successfully")
            
            # Step 4: Create RAG pipeline
            if status_callback:
                status_callback("Setting up RAG pipeline...")
            
            rag_pipeline = RAGPipeline()
            assistant = rag_pipeline.create_pipeline(documents, model_name, folder_path)
            
            # Step 5: Test the system
            if status_callback:
                status_callback("Testing system...")
            
            test_result = assistant.invoke({"query": "Say 'hello' briefly"})
            if not test_result or "result" not in test_result:
                raise Exception("System test failed")
            
            # Prepare folder info for UI
            folder_name = os.path.basename(folder_path)
            folder_info = f"Documents: {folder_name} ({len(documents)} files) • 🤖 Model: {model_name}"
            
            return assistant, folder_info
            
        except Exception as e:
            raise Exception(f"Initialization failed: {str(e)}")
    
    def get_all_text_files(self, folder_path):
        """Get all text files from folder and subfolders"""
        text_files = []
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.txt'):
                        text_files.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error scanning folder: {e}")
        return text_files
    
    def load_documents(self, text_files):
        """Load documents with robust loader"""
        documents = []
        for file_path in text_files:
            try:
                loader = RobustTextLoader(file_path, autodetect_encoding=True)
                file_docs = loader.load()
                if file_docs and file_docs[0].page_content.strip():
                    documents.extend(file_docs)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        return documents
    
    def create_sample_documents(self, folder_path):
        """Create sample documents if folder is empty"""
        sample_content = """Welcome to your custom RAG assistant!

This is a sample document that was created because the selected folder didn't contain any readable text files.

You can add your own .txt files to this folder and reinitialize the system to ask questions about your specific content.

Some example questions you can ask:
- What is this document about?
- What should I know about this content?
- Summarize the main points

Simply add your text files (.txt format) to the folder and click 'Change Documents' to reload."""
        
        sample_file = os.path.join(folder_path, "sample_document.txt")
        try:
            with open(sample_file, "w", encoding="utf-8") as f:
                f.write(sample_content)
            return sample_file
        except:
            return None
