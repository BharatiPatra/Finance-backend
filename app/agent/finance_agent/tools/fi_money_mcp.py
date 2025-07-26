import os
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

client = MCPClient(
    config={
        "mcpServers": {
            "playwright": {
                "url": f"http://localhost:8080/mcp/stream",
                "headers": {
                    "Mcp-Session-Id": "mcp-session-594e48ea-fea1-40ef-8c52-7552dd9272af"
                },
            }
        }
    }
)
# Create LLM
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.environ.get("OPENAI_API_KEY"),
)
# Create agent with tools
agent = MCPAgent(llm=llm, client=client, max_steps=10)


import asyncio


def fi_money_mcp_toolset(query: str):
    """
    Access the Fi Money MCP toolset to fetch up‑to‑date user financial data
    (net worth, credit reports, EPF balances, mutual fund transactions)
    Args:
        query (str): User query to be processed by MCP server.

    Returns:
        str: Personal finance detail based on user query
    """

    # Define an inner async function to call agent.run
    async def async_run():
        return await agent.run(query)

    # Run the async function synchronously
    result = asyncio.run(async_run())
    return result
