from typing import Any, Dict, List

import ollama

from edward.core.config import settings

_CLIENT = None


def get_llm_client() -> ollama.AsyncClient:
    """Return an asynchronous Ollama client."""
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = ollama.AsyncClient(host=settings.ollama_host)
    return _CLIENT


async def generate_response(
    messages: List[Dict[str, Any]], model: str | None = None
) -> str:
    """Generate a response from the LLM based on the conversation history."""
    client = get_llm_client()
    target_model = model or settings.model

    full_messages = [{"role": "system", "content": settings.system_prompt}] + messages

    try:
        response = await client.chat(model=target_model, messages=full_messages)
    except ollama.ResponseError as e:
        if e.status_code == 404:
            print(
                f"\nEdward: Downloading model {target_model}... this may take a moment."
            )
            await client.pull(target_model)
            response = await client.chat(model=target_model, messages=full_messages)
        else:
            raise
    return response["message"]["content"]
