import pytest

from edward.core.engine import run_bot


@pytest.mark.asyncio
async def test_run_bot(capsys):
    await run_bot()
    captured = capsys.readouterr()
    assert "Starting modern Edward async core..." in captured.out
    assert "Shutting down." in captured.out
