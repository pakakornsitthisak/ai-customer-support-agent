from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.llm import generate_response
from app.memory import clear_history


def test_generate_response_without_tool():
    session_id = "llm-test"

    clear_history(session_id)

    mock_response = SimpleNamespace(
        message=SimpleNamespace(
            content="Python is a programming language.",
            tool_calls=[],
        )
    )

    with patch(
        "app.llm.ollama_client.chat",
        return_value=mock_response,
    ) as mock_chat:
        result = generate_response(
            "What is Python?",
            session_id=session_id,
        )

    assert result == "Python is a programming language."

    mock_chat.assert_called_once()

    history = []

    from app.memory import get_history

    history = get_history(session_id)

    assert history == [
        {
            "role": "user",
            "content": "What is Python?",
        },
        {
            "role": "assistant",
            "content": "Python is a programming language.",
        },
    ]

    clear_history(session_id)


def test_generate_response_remembers_previous_conversation():
    session_id = "memory-test"

    clear_history(session_id)

    first_response = SimpleNamespace(
        message=SimpleNamespace(
            content="Python 3.13 introduced an experimental JIT compiler.",
            tool_calls=[],
        )
    )

    second_response = SimpleNamespace(
        message=SimpleNamespace(
            content="The JIT compiler can improve execution performance.",
            tool_calls=[],
        )
    )

    with patch(
        "app.llm.ollama_client.chat",
        side_effect=[
            first_response,
            second_response,
        ],
    ) as mock_chat:
        generate_response(
            "What is new in Python 3.13?",
            session_id=session_id,
        )

        result = generate_response(
            "What about its JIT compiler?",
            session_id=session_id,
        )

    assert result == ("The JIT compiler can improve execution performance.")

    assert mock_chat.call_count == 2

    # Check that the second request contains
    # the previous conversation.
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


@patch("app.llm.ollama_client.chat")
def test_agent_stops_after_max_tool_iterations(mock_chat):
    tool_response = MagicMock()

    tool_response.message.tool_calls = [
        MagicMock(
            function=MagicMock(
                name="calculate",
                arguments={"expression": "25 * 4"},
            )
        )
    ]

    mock_chat.return_value = tool_response

    session_id = "tool-limit-test"

    clear_history(session_id)

    result = generate_response(
        "Calculate 25 * 4",
        session_id=session_id,
    )

    assert "tool-call limit" in result.lower()

    assert mock_chat.call_count == 5

    clear_history(session_id)
