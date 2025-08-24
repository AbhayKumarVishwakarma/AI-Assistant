from fastapi import APIRouter, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.agent_service import run_agent
from app.auth.security import get_current_user


router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/chat", response_model=ChatResponse)
async def agent_route(req: ChatRequest):
    resp = run_agent(req.query)
    return ChatResponse(response=resp)

