# pip install -q -U google-genai to use gemini as a client

import os
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv
from libraries.PathRAG.utils import EmbeddingFunc
from libraries.PathRAG.PathRAG import PathRAG, QueryParam
from sentence_transformers import SentenceTransformer

import asyncio
import nest_asyncio
from libraries.PathRAG.llm import gpt_4o_mini_complete

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

WORKING_DIR = "./storage"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    # 1. Initialize the GenAI Client with your Gemini API Key
    client = genai.Client(api_key=gemini_api_key)

    # 2. Combine prompts: system prompt, history, and user prompt
    if history_messages is None:
        history_messages = []

    combined_prompt = ""
    if system_prompt:
        combined_prompt += f"{system_prompt}\n"

    for msg in history_messages:
        # Each msg is expected to be a dict: {"role": "...", "content": "..."}
        combined_prompt += f"{msg['role']}: {msg['content']}\n"

    # Finally, add the new user prompt
    combined_prompt += f"user: {prompt}"

    # 3. Call the Gemini model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )

    # 4. Return the response text
    return response.text


async def embedding_func(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


# api_key="your_api_key"
# os.environ["OPENAI_API_KEY"] = api_key
base_url = "https://api.openai.com/v1"
os.environ["OPENAI_API_BASE"] = base_url

rag = PathRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,
)
# rag = PathRAG(
#     working_dir=WORKING_DIR,
#     llm_model_func=llm_model_func,
#     embedding_func=EmbeddingFunc(
#         embedding_dim=384,
#         max_token_size=8192,
#         func=embedding_func,
#     ),
# )


def insert_document(file_path: str):
    with open(file_path, "r") as file:
        text = file.read()
    rag.insert(text)


def query_document(
    query: str, top_k: int = 5, response_type: str = "Multiple Paragraphs"
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


def main():
    # Initialize RAG instance
    # rag = asyncio.run(initialize_rag())
    file_path = "story.txt"
    with open(file_path, "r") as file:
        text = file.read()

    rag.insert(text)

    response = rag.query(
        query="What is the main theme of the story?",
        param=QueryParam(mode="hybrid", top_k=5, response_type="single line"),
    )

    print(response)


if __name__ == "__main__":
    main()
