"""
FastAPI routes for the chatbot.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.chatbot import process_chat

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.get("/")
def root():
    return {
        "message": "Welcome to the Real Estate AI Chatbot API"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/chat")
def chat(request: ChatRequest):
    response = process_chat(
    request.session_id,
    request.message,
)

    return {
        "response": response
    }