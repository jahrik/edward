import pytest
from unittest.mock import AsyncMock

from click.testing import CliRunner

from edward.cli import cli, coro


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Edward - Modernized Chatbot" in result.output


@pytest.mark.parametrize(
    "args, expected_model, expected_sp, expected_db",
    [
        (
            ["start"],
            "llama3.2:1b",
            "You are Edward, a terse and slightly sarcastic chatbot. Keep responses to 1 or 2 sentences max. Do not be overly helpful or offer unprompted advice.",
            "edward_memory.db",
        ),
        (
            [
                "start",
                "--model",
                "test-model",
                "--system-prompt",
                "test-prompt",
                "--db-path",
                "test-db",
            ],
            "test-model",
            "test-prompt",
            "test-db",
        ),
    ],
)
def test_start_command(mocker, runner, args, expected_model, expected_sp, expected_db):
    mock_run_bot = mocker.patch("edward.cli.run_bot", new_callable=AsyncMock)

    from edward.core.config import settings

    orig_model = settings.model
    orig_sp = settings.system_prompt
    orig_db = settings.db_path

    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    assert settings.model == expected_model
    assert settings.system_prompt == expected_sp
    assert settings.db_path == expected_db
    mock_run_bot.assert_called_once()

    settings.model = orig_model
    settings.system_prompt = orig_sp
    settings.db_path = orig_db


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (["export"], "edward_export.json"),
        (["export", "--output", "custom.json"], "custom.json"),
    ],
)
def test_export_command(mocker, runner, args, expected_output):
    mock_export = mocker.patch(
        "edward.core.memory.export_history", new_callable=AsyncMock
    )
    mock_close = mocker.patch("edward.core.memory.close_db", new_callable=AsyncMock)

    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    mock_export.assert_called_once_with(filepath=expected_output)
    mock_close.assert_called_once()
    assert f"Exporting history to {expected_output}..." in result.output


def test_coro_decorator():
    @coro
    async def dummy(x):
        return x * 2

    assert dummy(21) == 42
