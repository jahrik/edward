from aioconsole import ainput

from edward.core import llm, memory


async def run_shell_loop(model: str = "llama3.2:1b") -> None:
    """Run the interactive shell loop."""
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

        if not text:
            continue

        await memory.store_message("user", text)
        context = await memory.get_context(limit=10)

        try:
            response = await llm.generate_response(messages=context, model=model)
        except Exception as e:
            print(f"Edward: Error connecting to LLM ({e})")
            continue

        print(f"Edward: {response}")

        await memory.store_message("assistant", response)
