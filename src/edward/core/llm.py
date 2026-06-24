import os
from typing import Any, Dict, List

import ollama

DEFAULT_SYSTEM_PROMPT = "You are Edward, a terse and slightly sarcastic chatbot. Keep responses to 1 or 2 sentences max. Do not be overly helpful or offer unprompted advice."

_CLIENT = None


def get_llm_client() -> ollama.AsyncClient:
    """Return an asynchronous Ollama client."""
    global _CLIENT
    if _CLIENT is None:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        _CLIENT = ollama.AsyncClient(host=host)
    return _CLIENT


async def generate_response(
    messages: List[Dict[str, Any]], model: str = "llama3.2:1b"
) -> str:
    """Generate a response from the LLM based on the conversation history."""
    client = get_llm_client()

    sys_prompt = os.environ.get("EDWARD_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
    full_messages = [{"role": "system", "content": sys_prompt}] + messages

    try:
        response = await client.chat(model=model, messages=full_messages)
    except ollama.ResponseError as e:
        if e.status_code == 404:
            print(f"\nEdward: Downloading model {model}... this may take a moment.")
            await client.pull(model)
            response = await client.chat(model=model, messages=full_messages)
        else:
            raise
    return response["message"]["content"]
