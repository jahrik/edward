# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Purpose

"Edward" — a ~2019 chatbot that trained ChatterBot from Reddit (praw) and Twitter (tweepy) data stored in MongoDB, and chatted on Gitter/HipChat/voice. **Frozen learning archive**: ChatterBot is unmaintained, the Twitter streaming API and tweepy 3.x `StreamListener` are gone, Gitter/HipChat are dead, and the pinned requirements don't install on a current Python. The maintained bar is "compiles on current Python 3 and lints clean" — do not resurrect dependencies or port to new APIs unless explicitly asked.

## Commands

```bash
uv run edward start                            # start the bot
uv run edward --help                           # see available commands
ruff check .                                   # lint; config in pyproject.toml, CI runs the same
python3 -m py_compile $(git ls-files '*.py')   # syntax check
```

## Layout & quirks

- `src/edward/` — modern modular package with a `click` CLI entry point. Core (`src/edward/core/`) integrates `aiosqlite` for local Conversation RAG Memory and `ollama` for LLM interactions (`OLLAMA_HOST` defaults to `http://localhost:11434`).
- `edward.py` — original 2019 script with docopt CLI, training modes, etc. (kept untouched for historical archive purposes)
- `face_bot.py` — separate facepy/Facebook Graph experiment, partially commented out
- `mongo_functions.py` — mongo export helpers with hardcoded root/root localhost creds (archive artifact)
- The Dockerfile (`python:3.7.0a1-stretch` alpha base) and compose/stack files match the 2019 stack and are kept as-is for reference
- `list_5000` is training word-list data
