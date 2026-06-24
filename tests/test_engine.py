import pytest

from edward.core.engine import run_bot


@pytest.mark.asyncio
async def test_run_bot(capsys, mocker):
    mocker.patch("edward.core.engine.memory.init_db")
    mocker.patch("edward.core.engine.get_llm_client")

    await run_bot()
    captured = capsys.readouterr()
    assert "Starting modern Edward async core..." in captured.out
    assert "Initializing memory..." in captured.out
    assert "Connecting to Ollama..." in captured.out
    assert "Shutting down." in captured.out
