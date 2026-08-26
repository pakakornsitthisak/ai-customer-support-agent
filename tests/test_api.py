from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.generate_response")
def test_chat_success(mock_generate_response):
    mock_generate_response.return_value = "Python is a high-level programming language."

    response = client.post(
        "/chat",
        json={
            "message": "What is Python?",
            "session_id": "test-session",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == ("Python is a high-level programming language.")

    mock_generate_response.assert_called_once_with(
        message="What is Python?",
        session_id="test-session",
    )


@patch("app.main.generate_response")
def test_chat_default_session(mock_generate_response):
    mock_generate_response.return_value = "Test answer"

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"

    mock_generate_response.assert_called_once_with(
        message="Hello",
        session_id="default",
    )


def test_chat_without_message():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
        },
    )

    assert response.status_code == 422


@patch("app.main.clear_history")
def test_delete_session(mock_clear_history):
    response = client.delete("/sessions/test-session")

    assert response.status_code == 200

    assert response.json() == {
        "session_id": "test-session",
        "status": "cleared",
    }

    mock_clear_history.assert_called_once_with("test-session")
