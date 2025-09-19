from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

app = FastAPI()

@app.get("/")
def root():
    return {"Hello":"World"}

@app.get("/prompt/{prompt}") 
def get_prompt(prompt: str):
    result = llm.invoke(prompt)
    return {"response": result.content}
