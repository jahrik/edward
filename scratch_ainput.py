import asyncio
from aioconsole import ainput


async def main():
    try:
        try:
            await ainput("Prompt: ")
        except EOFError:
            print("EOF")
    finally:
        print("Cleanup")


asyncio.run(main())
