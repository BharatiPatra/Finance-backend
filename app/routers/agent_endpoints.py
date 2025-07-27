# routers/epf.py
import os
from pathlib import Path
import pathlib
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
import pdfplumber
from pydantic import BaseModel
from app.agent.finance_agent.main import run_agent


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "pdf"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

from pdfplumber.utils import exceptions as pdfplumber_exceptions


def reader_tool() -> str:
    file_path = UPLOAD_DIR / "file.pdf"
    if not file_path.exists():
        return "There is no file uploaded."

    page_texts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text(layout=True)
                if text:
                    page_texts.append(text)
    except pdfplumber_exceptions.PdfminerException as e:
        # Could be encrypted or corrupt
        return "Unable to read PDF: it may be password‑protected or corrupted."

    return "\n\n".join(page_texts)


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
    # 1) If they uploaded a PDF, save it and extract its text
    if file:
        file_path = UPLOAD_DIR / "file.pdf"
        with open(file_path, "wb") as out:
            out.write(await file.read())

        pdf_text = reader_tool()
        # 2) Prepend the PDF text to their question
        #    You can wrap it in a short header so the model knows what it is:
        combined = (
            "Here is the content of the PDF user just uploaded (layout and line breaks preserved):\n\n"
            f"{pdf_text}\n\n"
            "Now, please answer the user’s question below based on the above document:\n\n"
            "User query:"
            f"{message}"
        )
        print("Combined message:", combined)
    else:
        combined = message
    try:
        print("Running agent with request:", file)
        # Run the agent with the provided user ID, session ID, and message
        output = await run_agent(user_id, session_id, combined)
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
