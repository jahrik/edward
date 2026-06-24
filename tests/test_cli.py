from unittest.mock import AsyncMock

from click.testing import CliRunner

from edward.cli import cli, coro


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Edward - Modernized Chatbot" in result.output


def test_start_command(mocker):
    # Mock the run_bot function
    mock_run_bot = mocker.patch("edward.cli.run_bot", new_callable=AsyncMock)

    runner = CliRunner()
    result = runner.invoke(cli, ["start"])

    assert result.exit_code == 0
    mock_run_bot.assert_called_once()

    # Test with custom options
    from edward.core.config import settings

    # Save original
    orig_model = settings.model
    orig_sp = settings.system_prompt
    orig_db = settings.db_path

    mock_run_bot.reset_mock()
    result = runner.invoke(
        cli,
        [
            "start",
            "--model",
            "test-model",
            "--system-prompt",
            "test-prompt",
            "--db-path",
            "test-db",
        ],
    )
    assert result.exit_code == 0
    assert settings.model == "test-model"
    assert settings.system_prompt == "test-prompt"
    assert settings.db_path == "test-db"
    mock_run_bot.assert_called_once()

    # Restore
    settings.model = orig_model
    settings.system_prompt = orig_sp
    settings.db_path = orig_db


def test_export_command(mocker):
    # Mock memory.export_history and memory.close_db
    mock_export = mocker.patch(
        "edward.core.memory.export_history", new_callable=AsyncMock
    )
    mock_close = mocker.patch("edward.core.memory.close_db", new_callable=AsyncMock)

    runner = CliRunner()
    result = runner.invoke(cli, ["export"])

    assert result.exit_code == 0
    mock_export.assert_called_once_with(filepath="edward_export.json")
    mock_close.assert_called_once()
    assert "Exporting history to edward_export.json..." in result.output

    # Test with custom output
    mock_export.reset_mock()
    result = runner.invoke(cli, ["export", "--output", "custom.json"])
    assert result.exit_code == 0
    mock_export.assert_called_once_with(filepath="custom.json")
    assert "Exporting history to custom.json..." in result.output


def test_coro_decorator():
    @coro
    async def dummy(x):
        return x * 2

    assert dummy(21) == 42
