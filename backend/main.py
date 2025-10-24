from fastapi import FastAPI
from app.ai.gemini import GeminiModel
from dotenv import load_dotenv
from pydantic import BaseModel
import os  # Importe a biblioteca 'os'

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
