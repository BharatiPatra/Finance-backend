from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from app.agent.finance_agent.sub_agents.tax_advisor.agent import tax_advisor_agent

# from app.agent.finance_agent.tools.math_tools import math_tool_adk
from app.agent.finance_agent.sub_agents.search.agent import search_agent
from app.agent.finance_agent.sub_agents.investment_comparison.agent import (
    investment_comparison_agent,
)
from app.agent.finance_agent.prompt import (
    ROOT_PROMPT_DESCRIPTION,
    make_root_prompt,
)
from app.agent.finance_agent.tools.fi_money_mcp import fi_money_mcp_toolset

MODEL = "gemini-2.5-pro"


def get_root_agent():
    """
    Returns the root agent for the Finance Agent application.
    This agent is responsible for handling personal finance, tax queries, investment comparisons,
    market data retrieval.
    """
    return LlmAgent(
        name="PersonalFinanceAgent",
        model=MODEL,
        description=ROOT_PROMPT_DESCRIPTION,
        instruction=make_root_prompt(),
        output_key="output",
        tools=[
            AgentTool(agent=tax_advisor_agent),
            AgentTool(agent=search_agent),
            AgentTool(agent=investment_comparison_agent),
            fi_money_mcp_toolset,
            # math_tool_adk,
        ],
    )
