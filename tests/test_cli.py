from unittest.mock import AsyncMock, patch

from click.testing import CliRunner

from edward.cli import cli, coro


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Edward - Modernized Chatbot" in result.output


def test_start_command():
    runner = CliRunner()
    mock_run_bot = AsyncMock()
    with patch("edward.cli.run_bot", new=mock_run_bot):
        result = runner.invoke(cli, ["start"])
        assert result.exit_code == 0
        mock_run_bot.assert_called_once()


def test_coro_decorator():
    @coro
    async def dummy(x):
        return x * 2

    assert dummy(21) == 42
