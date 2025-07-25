# pip install -q -U google-genai to use gemini as a client

import os
from dotenv import load_dotenv
from libraries.PathRAG.PathRAG import PathRAG, QueryParam

import nest_asyncio
from libraries.PathRAG.llm import gpt_4o_mini_complete

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

load_dotenv()

WORKING_DIR = "./knowledge_base"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


# api_key="your_api_key"
# os.environ["OPENAI_API_KEY"] = api_key
base_url = "https://api.openai.com/v1"
os.environ["OPENAI_API_BASE"] = base_url

rag = PathRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)


def insert_document(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    rag.insert(text)


def query_document(
    query: str, top_k: int = 3, response_type: str = "Multiple Paragraphs"
):
    param = QueryParam(
        mode="hybrid",
        top_k=top_k,
        response_type=response_type,
    )
    response = rag.query(query=query, param=param)
    print(f"Query: {query}")
    print(f"Response: {response}")
    return response
