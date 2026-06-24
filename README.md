# Edward

[![CI](https://github.com/jahrik/edward/actions/workflows/ci.yml/badge.svg)](https://github.com/jahrik/edward/actions/workflows/ci.yml)

> **Frozen learning archive (built ~2019).** The services and libraries this bot was wired to are gone: ChatterBot is unmaintained, tweepy 3.x's `StreamListener` died with the old Twitter streaming API, and Gitter, HipChat, and the facepy Facebook Graph integration have all shut down or changed beyond recognition. The pinned `requirements.txt` no longer installs on a current Python. The code is kept compiling and lint-clean as reference material.

* A small bot that utilizes praw and chatterbot to connect to multiple services
* chatterbot: https://github.com/gunthercox/ChatterBot
* PRAW: https://praw.readthedocs.io/en/latest/

## Features
* **Ollama**: Seamlessly connects to a local or centralized homelab instance (e.g., Llama 3.2 3B or 3.1 8B).
* **Memory**: Uses a local SQLite database for Conversation RAG Memory.

## Dependencies
* Be sure to export envars first:
```bash
export OLLAMA_HOST="http://localhost:11434"
export EDWARD_SYSTEM_PROMPT="You are Edward, a terse and slightly sarcastic chatbot. Keep responses to 1 or 2 sentences max."
export REDDIT_CLIENT_ID=
export REDDIT_CLIENT_SECRET=
export REDDIT_USERNAME=
export REDDIT_PASSWORD=
export TWITTER_KEY=
export TWITTER_SECRET=
export TWITTER_TOKEN=
export TWITTER_TOKEN_SECRET=
export HIPCHAT_HOST=
export HIPCHAT_ROOM=
export HIPCHAT_ACCESS_TOKEN=
export GITTER_ROOM=
export GITTER_API_TOKEN=
```

## Usage

```bash
uv run edward start
uv run edward --help
```

*Note: The project has been modernized into a modular package under `src/edward/` with a `click` CLI. The original `edward.py` script is kept untouched for historical archive purposes.*

## Docker

Build and test with docker-compose:
```bash
make test
```

Build and deploy to docker swarm:
```bash
make deploy

docker stack services edward
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
i3laoiilqi76        edward_mongo        replicated          1/1                 mongo:latest        *:27017->27017/tcp
qyio6ac50xyt        edward_bot          replicated          1/1                 bot:latest
```
