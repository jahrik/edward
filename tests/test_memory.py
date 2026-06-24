import os
import tempfile
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from edward.core.memory import (
    close_db,
    get_context,
    init_db,
    store_message,
    export_history,
)


@pytest_asyncio.fixture
async def temp_db():
    fd, path = tempfile.mkstemp()
    os.close(fd)

    await init_db(path)
    yield path

    await close_db()
    os.remove(path)


@pytest.mark.asyncio
async def test_store_and_get_context(temp_db):
    await store_message("user", "Hello Edward")
    await store_message("assistant", "Hi there!")

    # Test getting all context
    context = await get_context()
    assert len(context) == 2
    assert context[0] == {"role": "user", "content": "Hello Edward"}
    assert context[1] == {"role": "assistant", "content": "Hi there!"}

    # Test limiting
    context_limit = await get_context(limit=1)
    assert len(context_limit) == 1
    assert context_limit[0] == {"role": "assistant", "content": "Hi there!"}


@pytest.mark.asyncio
async def test_get_context_with_query(temp_db):
    await store_message("user", "What is the capital of France?")
    await store_message("assistant", "The capital of France is Paris.")
    await store_message("user", "Who are you?")
    await store_message("assistant", "I am Edward.")

    # Test with query
    context = await get_context(query="capital")
    assert len(context) == 2
    assert context[1] == {
        "role": "assistant",
        "content": "The capital of France is Paris.",
    }


@pytest.mark.asyncio
async def test_get_context_empty_fts_query(temp_db):
    await store_message("user", "Hello")
    context = await get_context(query="!!! ???")
    assert len(context) == 0


@pytest.mark.asyncio
async def test_auto_init(mocker):
    fd, path = tempfile.mkstemp()
    os.close(fd)

    mocker.patch("edward.core.memory.DB_PATH", path)
    mocker.patch("edward.core.memory._CONN", None)

    await store_message("user", "Auto init test")

    mocker.patch("edward.core.memory._CONN", None)
    context = await get_context()

    assert len(context) == 1
    assert context[0]["content"] == "Auto init test"

    await close_db()
    os.remove(path)


@pytest.mark.asyncio
async def test_export_history(mocker, temp_db, tmp_path):
    await store_message("user", "test export")

    export_file = tmp_path / "test_export.json"
    await export_history(str(export_file))

    import json

    with open(export_file) as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["content"] == "test export"


@pytest.mark.asyncio
async def test_export_history_uninitialized(mocker, tmp_path):
    mocker.patch("edward.core.memory._CONN", None)
    mock_init = mocker.patch("edward.core.memory.init_db", new_callable=AsyncMock)
    mocker.patch(
        "edward.core.memory.get_context", new_callable=AsyncMock, return_value=[]
    )

    export_file = tmp_path / "test_uninit_export.json"
    await export_history(str(export_file))

    mock_init.assert_called_once()
