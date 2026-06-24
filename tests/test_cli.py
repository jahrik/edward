from unittest.mock import AsyncMock

from click.testing import CliRunner

from edward.cli import cli, coro


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Edward - Modernized Chatbot" in result.output


def test_start_command(mocker):
    # Mock the run_bot function so we don't actually start the event loop
    mock_run_bot = mocker.patch("edward.cli.run_bot", new_callable=AsyncMock)

    runner = CliRunner()
    result = runner.invoke(cli, ["start"])

    assert result.exit_code == 0
    mock_run_bot.assert_called_once()


def test_export_command(mocker):
    # Mock memory.export_history and memory.close_db
    mock_export = mocker.patch(
        "edward.core.memory.export_history", new_callable=AsyncMock
    )
    mock_close = mocker.patch("edward.core.memory.close_db", new_callable=AsyncMock)
    mock_print = mocker.patch("builtins.print")

    runner = CliRunner()
    result = runner.invoke(cli, ["export"])

    assert result.exit_code == 0
    mock_export.assert_called_once()
    mock_close.assert_called_once()
    mock_print.assert_any_call("Exporting history to edward_export.json...")
    mock_print.assert_any_call("Export complete.")


def test_coro_decorator():
    @coro
    async def dummy(x):
        return x * 2

    assert dummy(21) == 42
