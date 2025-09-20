from abc import ABC, abstractmethod

class AIPlatform(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Sends a prompt to the AI and returns the response text."""
        pass
    @abstractmethod
    def load_system_prompt() -> str:
        """Loads a predefined system prompt from a file."""
        pass

