"""
Main application window and controller
"""
import tkinter as tk
from tkinter import ttk
from .setup_frame import SetupFrame
from .chat_frame import ChatFrame

class RAGApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.assistant = None
        self.is_initialized = False
        self.setup_window()
        
    def setup_window(self):
        """Setup main application window"""
        self.root.title("Retrieval-Augmented Generation System")
        self.root.geometry("950x800")
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(main_frame, 
                               text="Retrieval-Augmented Generation - Ask Questions About Your Documents", 
                               font=('Arial', 14, 'bold'))
        header_label.pack(pady=10)
        
        # Setup frames
        self.setup_frame = SetupFrame(main_frame, self)
        self.chat_frame = ChatFrame(main_frame, self)
        
        # Show setup frame initially
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        
    def on_initialization_success(self, assistant, folder_info):
        """Handle successful initialization"""
        self.assistant = assistant
        self.is_initialized = True
        self.setup_frame.pack_forget()
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.chat_frame.on_system_ready(folder_info)
        
    def change_documents(self):
        """Return to setup screen to change documents"""
        self.is_initialized = False
        self.assistant = None
        self.chat_frame.pack_forget()
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_frame.reset_ui()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
