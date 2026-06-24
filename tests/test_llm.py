import os

import pytest
from ollama import AsyncClient

from edward.core.llm import generate_response, get_llm_client


def test_get_llm_client(mocker):
    mocker.patch("edward.core.llm._CLIENT", None)
    mocker.patch.dict(os.environ, {"OLLAMA_HOST": "http://test-host:11434"})
    client = get_llm_client()
    assert isinstance(client, AsyncClient)
    # The internal host might be formatted slightly differently but we verify it's an AsyncClient


def test_get_llm_client_default(mocker):
    mocker.patch("edward.core.llm._CLIENT", None)
    if "OLLAMA_HOST" in os.environ:
        mocker.patch.dict(os.environ, {}, clear=True)
    client = get_llm_client()
    assert isinstance(client, AsyncClient)


@pytest.mark.asyncio
async def test_generate_response(mocker):
    mock_client = mocker.MagicMock(spec=AsyncClient)

    # We need to mock the chat method which is an async method
    async def mock_chat(model, messages):
        return {"message": {"content": "mock response"}}

    mock_client.chat = mock_chat

    mocker.patch("edward.core.llm.get_llm_client", return_value=mock_client)

    messages = [{"role": "user", "content": "hello"}]
    response = await generate_response(messages)

    assert response == "mock response"


@pytest.mark.asyncio
async def test_generate_response_auto_pull(mocker):
    import ollama

    mock_client = mocker.MagicMock(spec=AsyncClient)

    call_count = 0

    async def mock_chat(model, messages):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ollama.ResponseError("model not found", status_code=404)
        return {"message": {"content": "pulled response"}}

    async def mock_pull(model):
        pass

    mock_client.chat = mock_chat
    mock_client.pull = mock_pull

    mocker.patch("edward.core.llm.get_llm_client", return_value=mock_client)

    messages = [{"role": "user", "content": "hello"}]
    response = await generate_response(messages)

    assert response == "pulled response"


@pytest.mark.asyncio
async def test_generate_response_other_error(mocker):
    import ollama

    mock_client = mocker.MagicMock(spec=AsyncClient)

    async def mock_chat(model, messages):
        raise ollama.ResponseError("server error", status_code=500)

    mock_client.chat = mock_chat
    mocker.patch("edward.core.llm.get_llm_client", return_value=mock_client)

    messages = [{"role": "user", "content": "hello"}]
    with pytest.raises(ollama.ResponseError):
        await generate_response(messages)
