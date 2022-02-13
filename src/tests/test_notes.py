import json
import pytest
from utils import status
from app.api import crud


def test_create_note(test_app, monkeypatch):
    test_request_payload = {
        "title": "test",
        "content": "test",
    }
    test_response_payload = {
        "id": 1,
        "title": "test",
        "content": "test",
    }

    async def mock_post(payload):
        return 1
    monkeypatch.setattr(crud, "post", mock_post)
    response = test_app.post("/api/notes/", data=json.dumps(test_request_payload))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    test_request_payload = {"title": "test"}
    response = test_app.post("/api/notes/", data=json.dumps(test_request_payload))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_note(test_app, monkeypatch):
    test_response_payload = {
        "id": 1,
        "title": "test",
        "content": "test",
    }

    async def mock_get(id):
        return test_response_payload
    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/api/notes/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_response_payload


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None
    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/api/notes/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # assert response.json() == "Note not found"
    assert response.json() == {"detail": "Note not found"}


def test_read_all_notes(test_app, monkeypatch):
    test_response_payload = [
        {
            "id": 1,
            "title": "test",
            "content": "test",
        },
        {
            "id": 2,
            "title": "test",
            "content": "test",
        },
    ]

    async def mock_get_all():
        return test_response_payload

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/api/notes/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_response_payload


def test_update_note(test_app, monkeypatch):
    test_request_payload = {
        "title": "test",
        "content": "test",
    }
    test_response_payload = {
        "id": 1,
        "title": "test",
        "content": "test",
    }

    async def mock_update(id, payload):
        return 1
    monkeypatch.setattr(crud, "update", mock_update)
    response = test_app.put("/api/notes/1", data=json.dumps(test_request_payload))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, status.HTTP_422_UNPROCESSABLE_ENTITY],
        [1, {"content": "test"}, status.HTTP_422_UNPROCESSABLE_ENTITY],
        [999, {"title": "test", "content": "bar"}, status.HTTP_404_NOT_FOUND],
    ]
)
def test_update_note_invalid_json(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None
    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.put(f"/api/notes/{id}", data=json.dumps(payload))
    assert response.status_code == status_code


def test_delete_note(test_app, monkeypatch):
    test_response_payload = {
        "id": 1,
        "title": "test",
        "content": "test",
    }

    async def mock_get(id):
        return test_response_payload

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/api/notes/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() == test_response_payload


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None
    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.delete("/api/notes/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Note not found"}
