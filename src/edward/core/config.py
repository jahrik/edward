import os
from dataclasses import dataclass


@dataclass
class Config:
    ollama_host: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model: str = os.environ.get("EDWARD_MODEL", "llama3.2:1b")
    system_prompt: str = os.environ.get(
        "EDWARD_SYSTEM_PROMPT",
        "You are Edward, a terse and slightly sarcastic chatbot. Keep responses to 1 or 2 sentences max. Do not be overly helpful or offer unprompted advice.",
    )
    db_path: str = os.environ.get("EDWARD_DB_PATH", "edward_memory.db")


settings = Config()
