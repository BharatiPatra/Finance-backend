# app/schemas/fi_mcp.py

from pydantic import BaseModel

class FiMCPRequest(BaseModel):
    """
    Schema for the request body when querying Fi Money MCP.
    """
    passcode: str
    query: str

class FiMCPResponse(BaseModel):
    """
    Schema for the response data from Fi Money MCP.
    (Adjust this based on the actual structure of data from Fi MCP)
    """
    data: dict # Using dict for now, but ideally a more specific schema