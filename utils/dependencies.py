"""
Dependency management and checking
"""
import subprocess
import sys

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "langchain",
        "langchain-community", 
        "langchain-huggingface",
        "langchain-ollama",
        "faiss-cpu",
        "sentence-transformers",
        "ollama",
        "chardet"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "langchain-huggingface":
                __import__("langchain_huggingface")
            elif package == "langchain-ollama":
                __import__("langchain_ollama")
            else:
                __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f" Missing dependencies: {', '.join(missing_packages)}")
        print("Installing required packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install packages. Please install them manually.")
            sys.exit(1)
    
    print("All dependencies are satisfied!")
