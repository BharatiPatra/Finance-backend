import os
import requests
import random
import uuid
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Request model
class ChatRequest(BaseModel):
    mcp_session_id: str


# Response model
class ChatResponse(BaseModel):
    is_success: bool
    user_id: str | None = None
    session_id: str | None = None
    mcp_session_id: str
    message: str | None = None
    login_url: str | None = None


@router.post("/login", response_model=ChatResponse)
def login(req: ChatRequest):
    mcp_session_id = req.mcp_session_id

    # Endpoint and headers
    url = os.getenv("MCP_SERVER_BASE_URL")
    headers = {"Content-Type": "application/json", "Mcp-Session-Id": mcp_session_id}

    # JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "fetch_bank_transactions", "arguments": {}},
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    try:
        data = response.json()
        print("Loaded data:", data)

        # Extract inner text from `content`
        if "result" in data and "content" in data["result"]:
            for item in data["result"]["content"]:
                if item.get("type") == "text":
                    inner_json = item.get("text")
                    parsed = None
                    try:
                        parsed = (
                            eval(inner_json)
                            if isinstance(inner_json, str)
                            else inner_json
                        )
                    except:
                        import json

                        parsed = json.loads(inner_json)

                    # Check if login is required
                    if parsed.get("status") == "login_required":
                        return {
                            "is_success": False,
                            "mcp_session_id": mcp_session_id,
                            "message": parsed.get("message"),
                            "login_url": parsed.get("login_url"),
                        }

        # If login is not required
        return {
            "is_success": True,
            "user_id": str(random.randint(1000, 9999)),
            "session_id": str(random.randint(1000, 9999)),
            "mcp_session_id": mcp_session_id,
        }

    except Exception as e:
        return {
            "is_success": False,
            "mcp_session_id": mcp_session_id,
            "message": f"Error parsing response: {str(e)}",
        }
