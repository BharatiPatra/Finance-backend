from app.agent.finance_agent.tools.tax_knowledge_base.knowledge_extractor import (
    query_document,
)


def tax_knowledge_base_tool(query: str) -> str:
    """Fetch tax-related information from the knowledge base.

    Args:
        query (str): The query string to search for.

    Returns:
        str: The response from the knowledge base.
    """
    return query_document(query)
