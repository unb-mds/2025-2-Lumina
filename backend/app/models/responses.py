from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


class RagRequest(BaseModel):
    prompt: str
    context: str


class RagResponse(BaseModel):
    response: str
