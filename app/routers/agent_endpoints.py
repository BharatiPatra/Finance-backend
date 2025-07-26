# routers/epf.py
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from app.agent.finance_agent.main import run_agent


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "pdf"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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
    if file:
        # Save the file to the upload directory
        file_path = UPLOAD_DIR / "file.pdf"
        # Save the uploaded file
        with open(file_path, "wb") as out:
            out.write(await file.read())
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
