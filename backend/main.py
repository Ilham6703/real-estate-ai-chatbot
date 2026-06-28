from fastapi import FastAPI

from backend.app.api import router


app = FastAPI(
    title="Real Estate AI Chatbot API",
    description="Backend API for the AI-powered Real Estate Chatbot",
    version="1.0.0",
)

app.include_router(router)