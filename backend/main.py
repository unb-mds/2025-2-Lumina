from fastapi import FastAPI
from app.services.scraping_manager import ScrapingManager
from app.ai.gemini import GeminiModel
from dotenv import load_dotenv
from pydantic import BaseModel
import os  

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = GeminiModel(api_key=GOOGLE_API_KEY)

app = FastAPI()

@app.post("/article/add")
def add_article(url: str):
   manager = ScrapingManager()
   
   article_id = manager.scrape_and_save(url)
   
   if article_id:
       return {"article_id": article_id}
   return {"message": "Article could not be saved."}

@app.get("/")
def root():
    return {"message": "The API is working!"}


@app.get("/prompt/{prompt}")
def response(prompt: str):
    return {"response": llm.chat(prompt)}


