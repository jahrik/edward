import ollama
import asyncio


async def test():
    client = ollama.AsyncClient()
    print(dir(client))


asyncio.run(test())
