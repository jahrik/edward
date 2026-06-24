import os
from typing import Any, Dict, List

import ollama

_CLIENT = None


def get_llm_client() -> ollama.AsyncClient:
    """Return an asynchronous Ollama client."""
    global _CLIENT
    if _CLIENT is None:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        _CLIENT = ollama.AsyncClient(host=host)
    return _CLIENT


async def generate_response(
    messages: List[Dict[str, Any]], model: str = "llama3"
) -> str:
    """Generate a response from the LLM based on the conversation history."""
    client = get_llm_client()
    response = await client.chat(model=model, messages=messages)
    return response["message"]["content"]
