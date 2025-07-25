# finance_agent/agents/investment_comparison_agent.py

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from app.agent.finance_agent.sub_agents.search.agent import search_agent
from app.agent.finance_agent.tools.math_tools import math_tool_adk
from app.agent.finance_agent.sub_agents.investment_comparison.prompt import (
    INVESTMENT_COMPARISON_DESCRIPTION,
    INVESTMENT_COMPARISON_PROMPT,
)

MODEL = "gemini-2.5-pro"

investment_comparison_agent = LlmAgent(
    name="InvestmentComparisonAgent",
    model=MODEL,
    description=INVESTMENT_COMPARISON_DESCRIPTION,
    instruction=INVESTMENT_COMPARISON_PROMPT,
    output_key="investment_comparison_output",
    tools=[
        AgentTool(agent=search_agent),
        math_tool_adk,
    ],
)
