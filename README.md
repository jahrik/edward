# Edward

[![CI](https://github.com/jahrik/edward/actions/workflows/ci.yml/badge.svg)](https://github.com/jahrik/edward/actions/workflows/ci.yml)

A modernized, asynchronous chatbot built with Python. Originally created in 2019 as a Reddit/Twitter bot using ChatterBot, Edward has been fully modernized from the ground up to utilize **Ollama** for blazing fast, local LLM inference and **SQLite** for persistent, Retrieval-Augmented Generation (RAG) conversation memory.

## Features

- **Modern Async Core**: Built entirely on `asyncio` for non-blocking I/O.
- **Local LLM Powered**: Integrates seamlessly with Ollama to run models like `llama3.2:1b` or `llama3.1:8b` locally without external API dependencies.
- **Auto-Pulling**: The Python client will automatically detect missing Ollama models and pull them via the API.
- **Persistent Memory**: A custom SQLite backend provides lightning fast conversation history (RAG) context.
- **Interactive REPL**: A responsive terminal shell loop using `aioconsole` that cleanly handles network disconnects and `Ctrl-C` exits.
- **Multi-Arch Deployment**: CI/CD automates `linux/amd64` and `linux/arm64` image builds using the blazing-fast `uv` runtime, ready for Docker Swarm.

## Architecture

```text
src/edward/
├── __init__.py
├── __main__.py          # Entry point for `python -m edward`
├── cli.py               # Click CLI commands and async hook
└── core/
    ├── engine.py        # Orchestration (init db, shell, shutdown)
    ├── llm.py           # Async Ollama client with auto-pull logic
    ├── memory.py        # SQLite RAG storage manager
    └── shell.py         # aioconsole interactive REPL loop
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for lightning-fast dependency management
- An [Ollama](https://ollama.com/) server running locally or on your homelab

## Configuration

Edward uses environment variables for configuration. Set these before starting the bot:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | The HTTP endpoint for the Ollama server |
| `EDWARD_SYSTEM_PROMPT` | `"You are Edward, a terse and slightly sarcastic chatbot. Keep responses to 1 or 2 sentences max."` | The base system prompt injected into every conversation |

*(Legacy credentials for Reddit/Twitter/Hipchat exist in history but are deprecated in the modern Shell MVP).*

## Usage

Start the interactive terminal loop:

```bash
uv run edward start
```

Edward will initialize the SQLite memory database (`edward_memory.db`) in the local directory, connect to Ollama, and present you with an interactive chat prompt. 

Special commands:
- `/quit` or `/exit`: Shut down gracefully.
- `/export`: Export your entire conversation history to `edward_export.json`.

```bash
# Start the bot
uv run edward start

# Start the bot with custom overrides
uv run edward start --model llama3.2:3b --db-path my_custom_memory.db

# Export the conversation history to JSON
uv run edward export
uv run edward export --output my_backup.json
```

For help and other commands:

```bash
uv run edward --help
```

## Docker Swarm Deployment

Edward is fully containerized for homelab deployments using a multi-arch `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` base image.

Deploy to your Swarm cluster:

```bash
docker stack deploy -c docker-stack.yml edward
```

The stack maps the SQLite database to a persistent volume and defaults the Ollama host to `http://ollama:11434`.

## Development & Testing

Edward maintains **100% test coverage** via `pytest-cov` and relies on `ruff` for linting and formatting.

To run the suite locally:

```bash
uv sync
uv run ruff check .
uv run ruff format .
uv run pytest --cov=src/edward --cov-report=term-missing
```

GitHub Actions automatically gates PRs against the test suite and builds the multi-arch image on push to `master`.

## License

MIT

## Author

jahrik@gmail.com
