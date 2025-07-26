# routers/epf.py
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from app.agent.finance_agent.main import run_agent


router = APIRouter()


# a dedicated response model
class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    reply: str


@router.post("/query", response_model=ChatResponse)
async def query_chat(
    user_id: str = Form(...),
    session_id: str = Form(...),
    message: str = Form(...),
    file: UploadFile | None = File(None),
):
    try:
        print("Running agent with request:", file)
        # Run the agent with the provided user ID, session ID, and message
        output = await run_agent(user_id, session_id, message)
        print("Agent output:", output)
        return ChatResponse(
            user_id=user_id,
            session_id=session_id,
            reply=output["output"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def test():
    return {"msg": "Hello World!"}
