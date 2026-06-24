from unittest.mock import AsyncMock

import pytest

from edward.core.shell import run_shell_loop


@pytest.mark.asyncio
async def test_run_shell_loop_quit(mocker):
    # Mock ainput to return "/quit"
    mocker.patch(
        "edward.core.shell.ainput", new_callable=AsyncMock, return_value="/quit"
    )

    await run_shell_loop()


@pytest.mark.asyncio
async def test_run_shell_loop_exit(mocker):
    # Mock ainput to return "/exit"
    mocker.patch(
        "edward.core.shell.ainput", new_callable=AsyncMock, return_value="/exit"
    )

    await run_shell_loop()


@pytest.mark.asyncio
async def test_run_shell_loop_eof(mocker):
    # Mock ainput to return None to simulate EOF logic from aioconsole depending on setup
    mocker.patch("edward.core.shell.ainput", new_callable=AsyncMock, return_value=None)

    await run_shell_loop()


@pytest.mark.asyncio
async def test_run_shell_loop_eoferror(mocker):
    # Mock ainput to raise EOFError
    mock_ainput = AsyncMock(side_effect=EOFError)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)

    await run_shell_loop()


@pytest.mark.asyncio
async def test_run_shell_loop_interaction(mocker):
    # Mock ainput to return "hello", then empty string, then "/exit"
    inputs = ["hello", " ", "/exit"]
    mock_ainput = AsyncMock(side_effect=inputs)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)

    # Mock memory and llm
    mock_store = mocker.patch(
        "edward.core.shell.memory.store_message", new_callable=AsyncMock
    )
    mock_get_context = mocker.patch(
        "edward.core.shell.memory.get_context",
        new_callable=AsyncMock,
        side_effect=[
            [{"role": "user", "content": "recent"}],  # First call: limit=10
            [
                {"role": "assistant", "content": "rag memory"}
            ],  # Second call: query="hello"
        ],
    )
    mock_generate = mocker.patch(
        "edward.core.shell.llm.generate_response",
        new_callable=AsyncMock,
        return_value="Hi there!",
    )

    # Mock print to verify output
    mock_print = mocker.patch("builtins.print")

    await run_shell_loop()

    assert mock_ainput.call_count == 3

    # Check that memory was updated correctly
    mock_store.assert_any_call("user", "hello")
    mock_store.assert_any_call("assistant", "Hi there!")
    assert mock_store.call_count == 2

    # Check context retrieval
    assert mock_get_context.call_count == 2
    mock_get_context.assert_any_call(limit=10)
    mock_get_context.assert_any_call(query="hello", limit=3)

    # Check LLM call includes the system RAG prompt
    expected_messages = [
        {
            "role": "system",
            "content": "Relevant past conversation memory:\n[assistant] rag memory",
        },
        {"role": "user", "content": "recent"},
    ]
    mock_generate.assert_called_once_with(
        messages=expected_messages, model="llama3.2:1b"
    )

    # Check print
    mock_print.assert_called_once_with("Edward: Hi there!")


@pytest.mark.asyncio
async def test_run_shell_loop_export(mocker, tmp_path):
    inputs = ["/export", "/exit"]
    mock_ainput = AsyncMock(side_effect=inputs)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)
    mock_export = mocker.patch(
        "edward.core.shell.memory.export_history",
        new_callable=AsyncMock,
    )
    mock_print = mocker.patch("builtins.print")

    await run_shell_loop()

    mock_export.assert_called_once()
    mock_print.assert_any_call("Edward: Exporting history to edward_export.json...")
    mock_print.assert_any_call("Edward: Export complete.")


@pytest.mark.asyncio
async def test_run_shell_loop_empty_response(mocker):
    inputs = ["hello", "/exit"]
    mock_ainput = AsyncMock(side_effect=inputs)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)
    mocker.patch("edward.core.shell.memory.store_message", new_callable=AsyncMock)
    mocker.patch(
        "edward.core.shell.memory.get_context", new_callable=AsyncMock, return_value=[]
    )
    mocker.patch(
        "edward.core.shell.llm.generate_response",
        new_callable=AsyncMock,
        return_value="  ",
    )
    mock_print = mocker.patch("builtins.print")

    await run_shell_loop()

    mock_print.assert_called_once_with("Edward: (Edward stares blankly)")


@pytest.mark.asyncio
async def test_run_shell_loop_keyboardinterrupt(mocker):
    # Mock ainput to raise KeyboardInterrupt
    mock_ainput = AsyncMock(side_effect=KeyboardInterrupt)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)

    await run_shell_loop()


@pytest.mark.asyncio
async def test_run_shell_loop_llm_exception(mocker):
    # Mock ainput to return "hello", then "/exit"
    inputs = ["hello", "/exit"]
    mock_ainput = AsyncMock(side_effect=inputs)
    mocker.patch("edward.core.shell.ainput", new=mock_ainput)

    # Mock memory
    mock_store = mocker.patch(
        "edward.core.shell.memory.store_message", new_callable=AsyncMock
    )
    mocker.patch(
        "edward.core.shell.memory.get_context", new_callable=AsyncMock, return_value=[]
    )

    # Mock llm to raise an exception
    mocker.patch(
        "edward.core.shell.llm.generate_response",
        new_callable=AsyncMock,
        side_effect=Exception("Connection refused"),
    )

    # Mock print
    mock_print = mocker.patch("builtins.print")

    await run_shell_loop()

    # Verify that the error was printed
    mock_print.assert_called_once_with(
        "Edward: Error connecting to LLM (Connection refused)"
    )

    # Verify that the user message was stored, but not the assistant message
    mock_store.assert_called_once_with("user", "hello")
