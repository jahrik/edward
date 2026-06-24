import asyncio
import click


def coro(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@coro
async def start():
    """Starts the Edward event loop."""
    pass


print(start.name)
print(start.help)
