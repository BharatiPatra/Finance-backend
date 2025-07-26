from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from app.agent.finance_agent.sub_agents.fi_money_mcp.prompt import (
    FI_MONEY_PROMPT,
    FI_MONEY_DESCRIPTION,
)

# from app.agent.finance_agent.tools.math_tools import math_tool_adk
from app.agent.finance_agent.tools.fi_money_mcp import get_fi_mcp_tools

MODEL = "gemini-2.5-pro"

fi_money_agent = LlmAgent(
    name="FIMoneyMCPAgent",
    model=MODEL,
    description=FI_MONEY_DESCRIPTION,
    instruction=FI_MONEY_PROMPT,
    output_key="fi_money_agent_output",
    tools=[get_fi_mcp_tools()],
)
