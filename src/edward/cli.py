import asyncio
import functools

import click

from edward.core.engine import run_bot


def coro(f):
    """Decorator to run async functions within click."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    """Edward - Modernized Chatbot"""
    pass


@cli.command()
@coro
async def start():
    """Starts the Edward event loop."""
    await run_bot()


@cli.command()
@coro
async def export():
    """Export the Edward conversation history to JSON."""
    from edward.core import memory

    print("Exporting history to edward_export.json...")
    await memory.export_history()
    print("Export complete.")
    await memory.close_db()
