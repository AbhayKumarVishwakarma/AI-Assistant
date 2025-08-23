from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.agent_service import run_agent


router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def agent_route(req: ChatRequest):
    resp = run_agent(req.query)
    return ChatResponse(response=resp)

