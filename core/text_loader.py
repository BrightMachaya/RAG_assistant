"""
Custom text loader with encoding detection
"""
import chardet
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document

class RobustTextLoader(TextLoader):
    """Custom text loader that handles encoding issues"""
    
    def __init__(self, file_path: str, encoding: str = None, autodetect_encoding: bool = True):
        self.file_path = file_path
        self.encoding = encoding
        self.autodetect_encoding = autodetect_encoding
        super().__init__(file_path)
    
    def load(self):
        """Load document with encoding detection"""
        try:
            if self.autodetect_encoding and self.encoding is None:
                # Detect encoding
                with open(self.file_path, 'rb') as file:
                    raw_data = file.read()
                    encoding_result = chardet.detect(raw_data)
                    self.encoding = encoding_result['encoding']
                    
                # Fallback to utf-8 if detection fails
                if self.encoding is None:
                    self.encoding = 'utf-8'
            
            # Try to load with detected encoding
            with open(self.file_path, 'r', encoding=self.encoding, errors='replace') as file:
                text = file.read()
            
            # Clean the text
            text = self.clean_text(text)
            
            return [Document(page_content=text, metadata={"source": self.file_path})]
            
        except Exception as e:
            print(f"Error loading {self.file_path}: {e}")
            # Return empty document instead of failing completely
            return [Document(page_content=f"Error loading this file: {str(e)}", metadata={"source": self.file_path})]
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Remove non-printable characters but keep common ones
        text = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
        return text
