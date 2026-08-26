from app.memory import (
    add_message,
    clear_history,
    get_history,
)


def test_add_and_get_history():
    session_id = "test-session"

    clear_history(session_id)

    add_message(
        session_id,
        "user",
        "Hello",
    )

    add_message(
        session_id,
        "assistant",
        "Hi there!",
    )

    history = get_history(session_id)

    assert history == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi there!",
        },
    ]

    clear_history(session_id)


def test_history_is_separated_by_session():
    session_a = "session-a"
    session_b = "session-b"

    clear_history(session_a)
    clear_history(session_b)

    add_message(
        session_a,
        "user",
        "Hello from A",
    )

    add_message(
        session_b,
        "user",
        "Hello from B",
    )

    assert get_history(session_a) == [
        {
            "role": "user",
            "content": "Hello from A",
        }
    ]

    assert get_history(session_b) == [
        {
            "role": "user",
            "content": "Hello from B",
        }
    ]

    clear_history(session_a)
    clear_history(session_b)


def test_history_keeps_only_last_10_messages():
    session_id = "limit-test"

    clear_history(session_id)

    for i in range(15):
        add_message(
            session_id,
            "user",
            f"Message {i}",
        )

    history = get_history(session_id)

    assert len(history) == 10
    assert history[0]["content"] == "Message 5"
    assert history[-1]["content"] == "Message 14"

    clear_history(session_id)


def test_clear_history():
    session_id = "clear-test"

    clear_history(session_id)

    add_message(
        session_id,
        "user",
        "Hello",
    )

    assert len(get_history(session_id)) == 1

    clear_history(session_id)

    assert get_history(session_id) == []
