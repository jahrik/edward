from aioconsole import ainput

from edward.core import llm, memory
from edward.core.config import settings


async def run_shell_loop(model: str | None = None) -> None:
    """Run the interactive shell loop."""
    target_model = model or settings.model
    while True:
        try:
            user_input = await ainput("You: ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input is None:
            break

        text = user_input.strip()
        if text.lower() in ("/quit", "/exit"):
            break

        if text.lower() == "/export":
            print("Edward: Exporting history to edward_export.json...")
            await memory.export_history()
            print("Edward: Export complete.")
            continue

        if not text:
            continue

        await memory.store_message("user", text)

        # Get recent sequential history
        recent_context = await memory.get_context(limit=10)

        # Get RAG context based on current query
        rag_context = await memory.get_context(query=text, limit=3)

        # Filter RAG to avoid duplicating what's already in recent history
        recent_contents = {msg["content"] for msg in recent_context}
        unique_rag = [
            msg for msg in rag_context if msg["content"] not in recent_contents
        ]

        final_context = []
        if unique_rag:
            rag_text = "Relevant past conversation memory:\n" + "\n".join(
                f"[{msg['role']}] {msg['content']}" for msg in unique_rag
            )
            final_context.append({"role": "system", "content": rag_text})

        final_context.extend(recent_context)

        try:
            response = await llm.generate_response(
                messages=final_context, model=target_model
            )
        except Exception as e:
            print(f"Edward: Error connecting to LLM ({e})")
            continue

        if not response or not response.strip():
            response = "(Edward stares blankly)"

        print(f"Edward: {response}")

        await memory.store_message("assistant", response)
