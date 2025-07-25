from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from app.agent.finance_agent.sub_agents.tax_advisor.prompt import (
    TAX_ADVISOR_PROMPT,
    TAX_ADVISOR_PROMPT_DESCRIPTION,
)
from app.agent.finance_agent.tools.math_tools import math_tool_adk
from app.agent.finance_agent.tools.fi_money_mcp import fi_money_mcp_toolset
from app.agent.finance_agent.tools.tax_knowledge_base_tool import (
    tax_knowledge_base_tool,
)

MODEL = "gemini-2.5-pro"

tax_advisor_agent = LlmAgent(
    name="TaxAdvisorAgent",
    model=MODEL,
    description=TAX_ADVISOR_PROMPT_DESCRIPTION,
    instruction=TAX_ADVISOR_PROMPT,
    output_key="tax_advisor_agent_output",
    tools=[
        tax_knowledge_base_tool,
    ],
)
