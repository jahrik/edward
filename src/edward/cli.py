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
    # This will hook into Phase 3's shell/chat loop
    await run_bot()
