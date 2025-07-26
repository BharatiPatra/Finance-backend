# routers/epf.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.finance_agent.main import run_agent


router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


# a dedicated response model
class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    reply: str


@router.post("/query", response_model=ChatResponse)
def query_chat(request: ChatRequest):
    try:
        # Run the agent with the provided user ID, session ID, and message
        output = run_agent(request.user_id, request.session_id, request.message)
        return ChatResponse(
            user_id=request.user_id,
            session_id=request.session_id,
            reply=output["output"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def test():
    return {"msg": "Hello World!"}
