from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat():
    response = client.post(
        "/chat",
        json={
            "message": "What is 125 * 48?",
            "session_id": "test-session",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "6000" in data["answer"]


def test_delete_session():
    response = client.delete("/sessions/test-session")

    assert response.status_code == 200

    assert response.json() == {
        "session_id": "test-session",
        "status": "cleared",
    }
