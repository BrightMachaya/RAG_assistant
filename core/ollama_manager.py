"""
Ollama model management
"""
import subprocess

class OllamaManager:
    """Manager for Ollama operations"""
    
    @staticmethod
    def check_ollama_installed():
        """Check if Ollama is installed and accessible"""
        try:
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    @staticmethod
    def get_available_models():
        """Get list of available Ollama models"""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                models = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    @staticmethod
    def pull_model(model_name):
        """Pull a model if not available"""
        try:
            print(f"Pulling model: {model_name}")
            result = subprocess.run(["ollama", "pull", model_name], capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False
    
    @staticmethod
    def is_model_available(model_name):
        """Check if specific model is available"""
        available_models = OllamaManager.get_available_models()
        return any(model_name in model for model in available_models)
