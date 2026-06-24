# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Purpose

"Edward" is an asynchronous chatbot built with Python. Originally created in 2019, Edward has been fully modernized to utilize **Ollama** for blazing fast, local LLM inference and **SQLite** for persistent, Retrieval-Augmented Generation (RAG) conversation memory. The codebase relies on a modern `uv` stack, `asyncio`, and `click` for the CLI.

## Commands

```bash
uv run edward start                            # start the bot
uv run edward --help                           # see available commands
ruff check .                                   # lint; config in pyproject.toml, CI runs the same
python3 -m py_compile $(git ls-files '*.py')   # syntax check
```

## Layout & quirks

- `src/edward/` — modern modular package with a `click` CLI entry point. Core (`src/edward/core/`) integrates `aiosqlite` for local Conversation RAG Memory and `ollama` for LLM interactions (`OLLAMA_HOST` defaults to `http://localhost:11434`).
- Docker Swarm deployment is configured via `docker-stack.yml` and the modern multi-arch `Dockerfile` utilizing a `uv` base.
