import os  # Importe a biblioteca 'os'

from dotenv import load_dotenv
from fastapi import FastAPI

from app.ai.gemini import GeminiModel

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = GeminiModel(api_key=GOOGLE_API_KEY)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "The API is working!"}


@app.get("/prompt/{prompt}")
def response(prompt: str):
    return {"response": llm.chat(prompt)}
