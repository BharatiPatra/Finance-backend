from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from app.agent.finance_agent.sub_agents.search.prompt import (
    SEARCH_PROMPT,
    SEARCH_AGENT_DESCRIPTION,
)

MODEL = "gemini-2.5-pro"

search_agent = LlmAgent(
    name="SearchAgent",
    model=MODEL,
    description=SEARCH_AGENT_DESCRIPTION,
    instruction=SEARCH_PROMPT,
    output_key="search_agent_output",
)
