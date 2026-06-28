from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Welcome to the Real Estate AI Chatbot API!"
    }


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@router.post("/chat")
async def chat():
    return {
        "response": "Chat endpoint coming soon."
    }