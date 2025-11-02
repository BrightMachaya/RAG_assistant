"""
Setup frame for document selection and initialization
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from core.ollama_manager import OllamaManager
from core.document_processor import DocumentProcessor

class SetupFrame(ttk.LabelFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, text="Step 1: Setup & Document Selection", padding="15")
        self.app_controller = app_controller
        self.ollama_manager = OllamaManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components"""
        # Document selection
        doc_selection_frame = ttk.Frame(self)
        doc_selection_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(doc_selection_frame, text="Select Documents Folder:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Folder path with browse button
        path_frame = ttk.Frame(doc_selection_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        self.doc_path_var = tk.StringVar(value="Click 'Browse' to select folder")
        self.path_entry = ttk.Entry(path_frame, textvariable=self.doc_path_var, width=70, state='readonly')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side=tk.RIGHT)
        
        # Supported files info
        ttk.Label(doc_selection_frame, text="Supported: .txt files (other files will be skipped)",
                 foreground='gray', font=('Arial', 9)).pack(anchor=tk.W, pady=2)
        
        # Model selection
        self.setup_model_selection()
        
        # Initialize button
        self.init_btn = ttk.Button(self, text="INITIALIZE RAG SYSTEM", 
                                 command=self.initialize_system, style="Big.TButton")
        self.init_btn.pack(pady=15)
        
        # Status
        self.status_var = tk.StringVar(value="Select a documents folder and click Initialize")
        status_label = ttk.Label(self, textvariable=self.status_var, 
                               foreground='blue', font=('Arial', 10))
        status_label.pack(pady=5)
        
        # Configure styles
        style = ttk.Style()
        style.configure('Big.TButton', font=('Arial', 12, 'bold'), padding=10)
        
    def setup_model_selection(self):
        """Setup model selection components"""
        model_frame = ttk.Frame(self)
        model_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(model_frame, text="Select AI Model:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        self.model_var = tk.StringVar(value="llama2")
        
        # Get available models
        available_models = self.ollama_manager.get_available_models()
        default_models = ["llama2", "mistral", "codellama", "phi", "gemma", "llama3", "qwen2"]
        
        # Combine available models with defaults
        all_models = list(set(available_models + default_models))
        all_models.sort()
        
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                  values=all_models, state="readonly", width=20)
        model_combo.pack(anchor=tk.W, pady=5)
        
        # Model status
        self.model_status_var = tk.StringVar(value="Select a model")
        model_status_label = ttk.Label(model_frame, textvariable=self.model_status_var,
                                     font=('Arial', 9))
        model_status_label.pack(anchor=tk.W, pady=2)
        
        # Update model status when selection changes
        model_combo.bind('<<ComboboxSelected>>', self.on_model_selected)
        self.update_model_status()
        
    def on_model_selected(self, event=None):
        """Update model status when selection changes"""
        self.update_model_status()
        
    def update_model_status(self):
        """Update the model availability status"""
        selected_model = self.model_var.get()
        if self.ollama_manager.is_model_available(selected_model):
            self.model_status_var.set("Model available")
        else:
            self.model_status_var.set("Model not downloaded - will attempt to pull")
            
    def browse_folder(self):
        """Open folder selection dialog"""
        folder_path = filedialog.askdirectory(
            title="Select Folder Containing Documents",
            initialdir=os.getcwd()
        )
        
        if folder_path:
            self.doc_path_var.set(folder_path)
            supported_files, total_files = self.scan_folder(folder_path)
            if supported_files == 0:
                self.status_var.set(f" No .txt files found. I'll create a sample document.")
            else:
                self.status_var.set(f"Found {supported_files} supported file(s) out of {total_files} total files")
                
    def scan_folder(self, folder_path):
        """Scan folder for supported files"""
        try:
            all_files = []
            supported_files = []
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    all_files.append(file)
                    if file.lower().endswith('.txt'):
                        supported_files.append(os.path.join(root, file))
            
            return len(supported_files), len(all_files)
        except:
            return 0, 0
            
    def initialize_system(self):
        """Initialize the RAG system with selected folder"""
        folder_path = self.doc_path_var.get()
        
        if not folder_path or folder_path == "Click 'Browse' to select folder":
            messagebox.showwarning("Selection Required", "Please select a documents folder first.")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
            return
        
        # Check Ollama installation
        if not self.ollama_manager.check_ollama_installed():
            messagebox.showerror("Ollama Not Found", 
                               "Ollama 1.0.1 is not installed or not in PATH.\n\n"
                               "Please install Ollama from https://ollama.ai/ and ensure it's running.")
            return
        
        self.init_btn.config(state=tk.DISABLED)
        self.status_var.set("Initializing... Please wait...")
        
        # Run in separate thread
        threading.Thread(target=self._initialize_backend, args=(folder_path,), daemon=True).start()
        
    def _initialize_backend(self, folder_path):
        """Initialize backend components in background thread"""
        try:
            selected_model = self.model_var.get()
            document_processor = DocumentProcessor()
            
            # Initialize the system
            assistant, folder_info = document_processor.initialize_system(
                folder_path, selected_model, self.update_status
            )
            
            # Notify main application
            self.app_controller.root.after(0, 
                lambda: self.app_controller.on_initialization_success(assistant, folder_info)
            )
            
        except Exception as e:
            error_msg = f"Initialization failed: {str(e)}"
            self.app_controller.root.after(0, 
                lambda: self.status_var.set(f"{error_msg}")
            )
            self.app_controller.root.after(0, 
                lambda: self.init_btn.config(state=tk.NORMAL)
            )
            self.app_controller.root.after(0, 
                lambda: messagebox.showerror("Initialization Error", str(e))
            )
            
    def update_status(self, message):
        """Update status message from background thread"""
        self.app_controller.root.after(0, lambda: self.status_var.set(message))
        
    def reset_ui(self):
        """Reset UI to initial state"""
        self.status_var.set("Select a documents folder and click Initialize")
        self.init_btn.config(state=tk.NORMAL)
