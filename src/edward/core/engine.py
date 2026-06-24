import asyncio

from edward.core import memory
from edward.core.llm import get_llm_client


async def run_bot():
    """Main execution loop for Edward."""
    print("Starting modern Edward async core...")

    # 1. Setup SQLite memory (Phase 2)
    print("Initializing memory...")
    await memory.init_db()

    # 2. Setup Ollama client (Phase 2)
    print("Connecting to Ollama...")
    llm_client = get_llm_client()  # noqa: F841

    # 3. Start interaction loop (Phase 3)
    # For now, just test the initialization

    await asyncio.sleep(0.1)  # Placeholder
    print("Shutting down.")
