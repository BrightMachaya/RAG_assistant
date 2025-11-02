"""
Chat interface for asking questions
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

class ChatFrame(ttk.LabelFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, text="Step 2: Ask Questions", padding="15")
        self.app_controller = app_controller
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the chat interface"""
        # Document info
        self.doc_info_var = tk.StringVar(value="No documents loaded")
        doc_info_label = ttk.Label(self, textvariable=self.doc_info_var,
                                  foreground='green', font=('Arial', 10, 'bold'))
        doc_info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Chat display
        chat_display_frame = ttk.Frame(self)
        chat_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_display_frame, 
            wrap=tk.WORD, 
            width=85, 
            height=18,
            font=('Arial', 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags
        self.chat_display.tag_config("user", foreground="blue", font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("assistant", foreground="green", font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("system", foreground="purple")
        
        # Input area
        self.setup_input_area()
        
        # Sample questions
        self.setup_sample_questions()
        
    def setup_input_area(self):
        """Setup question input area"""
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Your question:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.question_var = tk.StringVar()
        self.question_entry = ttk.Entry(input_frame, textvariable=self.question_var, 
                                       width=70, font=('Arial', 10))
        self.question_entry.pack(fill=tk.X, pady=5)
        self.question_entry.bind('<Return>', self.on_enter_pressed)
        
        # Buttons frame
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.ask_btn = ttk.Button(btn_frame, text="Ask Question", 
                                command=self.ask_question, state=tk.DISABLED)
        self.ask_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_frame, text="Clear Chat", command=self.clear_chat).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Change Documents", 
                  command=self.app_controller.change_documents).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Exit", command=self.app_controller.root.quit).pack(side=tk.LEFT)
        
    def setup_sample_questions(self):
        """Setup sample questions frame"""
        sample_frame = ttk.LabelFrame(self.app_controller.root, text="Sample Questions", padding="10")
        
        sample_questions = [
            "What are the main topics in these documents?",
            "Summarize the key points",
            "Explain the most important concepts",
            "What should I know about this content?"
        ]
        
        for question in sample_questions:
            btn = ttk.Button(sample_frame, text=question,
                           command=lambda q=question: self.insert_sample_question(q))
            btn.pack(fill=tk.X, pady=2)
            
    def on_system_ready(self, folder_info):
        """Called when system is ready for questions"""
        self.doc_info_var.set(folder_info)
        self.ask_btn.config(state=tk.NORMAL)
        self.question_entry.focus()
        self.add_message("system", "RAG system ready! Ask me anything about your documents!")
        
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        self.ask_question()
        return "break"
        
    def insert_sample_question(self, question):
        """Insert sample question into input field"""
        if not self.app_controller.is_initialized:
            messagebox.showwarning("Not Ready", "Please initialize the RAG system first.")
            return
        
        self.question_var.set(question)
        self.question_entry.focus()
        
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "Assistant: ", "assistant")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "system":
            self.chat_display.insert(tk.END, f"{message}\n\n", "system")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("system", "Chat cleared. Ready for new questions.")
        
    def ask_question(self):
        """Ask question to the RAG system"""
        if not self.app_controller.is_initialized:
            messagebox.showwarning("Not Ready", "Please initialize the RAG system first.")
            return
        
        question = self.question_var.get().strip()
        if not question:
            messagebox.showwarning("Input Error", "Please enter a question.")
            return
        
        # Clear input and disable button
        self.question_var.set("")
        self.ask_btn.config(state=tk.DISABLED)
        self.question_entry.config(state=tk.DISABLED)
        
        # Add user question
        self.add_message("user", question)
        self.add_message("system", "Thinking...")
        
        # Process in background
        threading.Thread(target=self._process_question, args=(question,), daemon=True).start()
        
    def _process_question(self, question):
        """Process question in background"""
        try:
            result = self.app_controller.assistant.invoke({"query": question})
            answer = result["result"]
            sources = result.get("source_documents", [])
            
            self.app_controller.root.after(0, 
                lambda: self._show_response(answer, sources)
            )
            
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            self.app_controller.root.after(0, 
                lambda: self._show_error(error_msg)
            )
            
    def _show_response(self, answer, source_documents):
        """Show response in chat"""
        self._remove_thinking_message()
        self.add_message("assistant", answer)
        
        if source_documents:
            sources_info = f"\n Sources referenced: {len(source_documents)} document(s)"
            self.add_message("system", sources_info)
            
        self.ask_btn.config(state=tk.NORMAL)
        self.question_entry.config(state=tk.NORMAL)
        self.question_entry.focus()
        
    def _show_error(self, error_msg):
        """Show error message"""
        self._remove_thinking_message()
        self.add_message("system", f" {error_msg}")
        self.ask_btn.config(state=tk.NORMAL)
        self.question_entry.config(state=tk.NORMAL)
        self.question_entry.focus()
        
    def _remove_thinking_message(self):
        """Remove the thinking message from chat"""
        self.chat_display.config(state=tk.NORMAL)
        content = self.chat_display.get("1.0", tk.END)
        if "Thinking..." in content:
            lines = content.split('\n')
            new_content = []
            skip_next = False
            for line in lines:
                if "Thinking..." in line:
                    skip_next = True
                    continue
                if skip_next and line == "":
                    skip_next = False
                    continue
                new_content.append(line)
            
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.insert("1.0", '\n'.join(new_content))
        self.chat_display.config(state=tk.DISABLED)
