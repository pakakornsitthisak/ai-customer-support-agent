from unittest.mock import MagicMock, patch

from app.llm import generate_response
from app.memory import clear_history


@patch("app.llm.ollama_client.chat")
def test_agent_remembers_previous_message(mock_chat):
    session_id = "memory-test"

    clear_history(session_id)

    # First response
    first_response = MagicMock()
    first_response.message.tool_calls = []
    first_response.message.content = (
        "Python 3.13 introduced an experimental JIT compiler."
    )

    # Second response
    second_response = MagicMock()
    second_response.message.tool_calls = []
    second_response.message.content = "The JIT compiler in Python 3.13 is experimental."

    mock_chat.side_effect = [
        first_response,
        second_response,
    ]

    first_result = generate_response(
        "What is new in Python 3.13?",
        session_id=session_id,
    )

    second_result = generate_response(
        "What about its JIT compiler?",
        session_id=session_id,
    )

    assert first_result == ("Python 3.13 introduced an experimental JIT compiler.")

    assert second_result == ("The JIT compiler in Python 3.13 is experimental.")

    # Inspect the messages sent to Ollama during the second call.
    second_call_messages = mock_chat.call_args_list[1].kwargs["messages"]

    assert {
        "role": "user",
        "content": "What is new in Python 3.13?",
    } in second_call_messages

    assert {
        "role": "assistant",
        "content": ("Python 3.13 introduced an experimental JIT compiler."),
    } in second_call_messages

    assert {
        "role": "user",
        "content": "What about its JIT compiler?",
    } in second_call_messages

    clear_history(session_id)
