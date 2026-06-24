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
@click.option("--model", help="The LLM model to use.")
@click.option("--system-prompt", help="The system prompt for Edward.")
@click.option("--db-path", help="Path to the SQLite database.")
@coro
async def start(model: str | None, system_prompt: str | None, db_path: str | None):
    """Starts the Edward event loop."""
    from edward.core.config import settings

    if model:
        settings.model = model
    if system_prompt:
        settings.system_prompt = system_prompt
    if db_path:
        settings.db_path = db_path

    await run_bot()


@cli.command()
@click.option(
    "--output", "-o", default="edward_export.json", help="Path to the output JSON file."
)
@coro
async def export(output: str):
    """Export the Edward conversation history to JSON."""
    from edward.core import memory

    click.echo(f"Exporting history to {output}...")
    await memory.export_history(filepath=output)
    click.echo("Export complete.")
    await memory.close_db()
