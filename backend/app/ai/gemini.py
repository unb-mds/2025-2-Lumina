from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from app.ai.ai_models.AIPlatform import AIPlatform


class GeminiModel(AIPlatform):
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.model_name: str = "gemini-2.5-flash"
        self.llm = ChatGoogleGenerativeAI(model=self.model_name)
        self.system_prompt: str = self.load_system_prompt()

    def chat(self, prompt: str) -> str:
        prompt = f"System_Prompt:{self.system_prompt}\n\nUser_prompt: {prompt}:"
        response = self.llm.invoke(prompt)
        return response.content

    def load_system_prompt(self) -> str:
        prompt_path = Path(__file__).parent / "system_prompts" / "system_prompt.md"
        with open(prompt_path) as file:
            return file.read()
