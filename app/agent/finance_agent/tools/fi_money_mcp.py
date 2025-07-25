from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

fi_money_mcp_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://localhost:8080/mcp/stream",
        headers={"Mcp-Session-Id": "mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af"},
    )
)
