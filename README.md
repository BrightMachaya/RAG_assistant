## RETRIEVAL AUGMENTED GENERATION SYSTEM with Ollama



### Overview



This project is a standalone RAG system with a Tkinter-based GUI that allows you to load .txt documents, 



create embeddings using HuggingFace models, and query them using Ollama LLMs such as llama2, mistral, phi, etc.



**It automatically handles**.



\*Document loading and cleaning



\*Chunking and embedding



\*Vector storage via FAISS



\*Retrieval and LLM-based response generation



\*Dynamic model management and live chat interface



 *Everything runs locally — no cloud API required once Ollama is installed*.



### Features



\*Retrieval-Augmented Generation (RAG) pipeline using LangChain



\*Interactive GUI built with Tkinter



\*Load .txt documents from any folder



\*FAISS vector database for fast semantic retrieval



\*HuggingFace embeddings (all-MiniLM-L6-v2)



\*Ollama 1.0.1 integration for local LLM inference



\*Auto-handling of encoding issues (via chardet)



\*Optional sample document creation if folder is empty



\*Persistent vector store per document folder



### Prerequisites



Python 3.8 or higher



Ollama installed and running



At least 8GB RAM (16GB recommended for larger document collections)



### Installation



git clone https://github.com/BrightMachaya/RAG\_assistant.git



cd RAG\_assistant



run ollama pull e.g, llama2, mistral, phi for language models



pip install langchain-community faiss-cpu sentence-transformers ollama chardet



### Run the RAG system



python main.py



**Steps in the GUI App**



1\. Browse a Folder containing .txt documents.



2\. Choose an Ollama Model (e.g., llama2, mistral, phi).



3\. Click “INITIALIZE RAG SYSTEM” — this will:

&nbsp;  Check/install the model (if not available)

&nbsp;  Load and embed documents

&nbsp;  Build or load a FAISS vector store



4\. Start asking questions via the chat box!



### Advanced Features



#### Enhanced Query Processing



**Smart Chunking**: Documents are split into 1000-character chunks with 200-character overlap for optimal context preservation



**Encoding Detection**: Automatic detection and handling of various text encodings



**Error Resilience**: Continues processing even if some files fail to load



#### Retrieval Evaluation



The system provides comprehensive feedback on:



**Document Loading Status**: Shows successful vs failed file loads



**Processing Statistics**: Number of documents processed and chunks created



**Real-time Performance**: Search latency and retrieval metrics



#### RAG Environment Configuration



**Vector Store Management**: Automatic creation and loading of FAISS indices



**Model Selection**: Support for multiple Ollama LLMs



**Memory Optimization**: Efficient chunking and embedding strategies



#### Project Scope \& Capabilities



**Document Types**: Currently supports .txt files with robust encoding handling



**Scalability**: Efficiently handles hundreds of documents



**Cross-Platform**: Works on Windows, Mac, and Linux



**Offline Operation**: No internet connection required after setup



### Configuration Management



The system automatically manages:



**Vector Store Paths**: Unique storage for each document folder



**Model Settings**: Configurable chunk sizes and retrieval parameters



**Session Management**: Persistent vector stores between sessions



### Use Cases



**Academic Research**: Query research papers and academic documents



**Legal Document Analysis**: Search through case files and legal documents



**Enterprise Knowledge Bases**: Internal documentation search



**Personal Document Management**: Organize and query personal files



**Content Analysis**: Extract insights from large text collections



### Troubleshooting



#### Common Issues



**Ollama Not Found**:



Ensure Ollama is installed and running



Check that models are downloaded (ollama list)



**FAISS Installation Issues**:



Try: pip install faiss-cpu --no-cache-dir --force-reinstall



On Windows, ensure Microsoft C++ Build Tools are installed



**Document Loading Errors**:



The system will create sample documents if none are found



Check file encodings - the system handles most common encodings automatically



#### Performance Tips



Use SSD storage for faster vector store operations



Close other memory-intensive applications during initialization



For large document collections, consider increasing system RAM



### Future Enhancements



Planned improvements include:



Support for PDF, DOCX, and HTML documents



Advanced retrieval evaluation metrics



Configurable chunking strategies



Batch processing for large document collections



Export capabilities for search results



### Contributing



We welcome contributions! Please feel free to submit pull requests or open issues for:



Bug reports



Feature requests



Documentation improvements



Performance enhancements



### License



This project is licensed under the MIT License - see the LICENSE file for details.



### Acknowledgments



FAISS for efficient similarity search



LangChain for the RAG framework



Ollama for local LLM inference



Hugging Face for embedding models





### Support



Create an issue for bug reports



Check the troubleshooting section for common solutions



Ensure all prerequisites are properly installed







**Author**

Bright Machaya



If you find this project useful, please give it a star ⭐

