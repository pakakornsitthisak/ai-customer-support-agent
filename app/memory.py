from collections import defaultdict


MAX_HISTORY_MESSAGES = 10

_history: dict[str, list[dict[str, str]]] = defaultdict(list)


def add_message(
    session_id: str,
    role: str,
    content: str,
) -> None:
    """Store a conversation message."""

    _history[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )

    # Keep only the most recent messages.
    _history[session_id] = _history[session_id][-MAX_HISTORY_MESSAGES:]


def get_history(session_id: str) -> list[dict[str, str]]:
    """Return conversation history for a session."""

    return _history[session_id].copy()


def clear_history(session_id: str) -> None:
    """Clear conversation history for a session."""

    _history.pop(session_id, None)
