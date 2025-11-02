#!/usr/bin/env python3
"""
Main entry point for the RAG Assistant Application
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import RAGApplication

def main():
    """Launch the RAG Assistant application"""
    try:
        app = RAGApplication()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
