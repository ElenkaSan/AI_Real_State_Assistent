from fastapi import APIRouter
from app.core.memory import reset_memory

router = APIRouter()

@router.post("/")
async def reset_conversation():
    reset_memory()
    return {"message": "Conversation memory cleared."}
