import pytest
from fastapi.testclient import TestClient

import categorizer
import database
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "test.db"))
    monkeypatch.setattr(categorizer, "_cache", {})
    database.init_db()
    return TestClient(app)


def test_validate_cleans_markdown_reply():
    assert categorizer._validate("**Food** for this expense") == "Food"


def test_validate_rejects_unknown_category():
    assert categorizer._validate("Spaceships") == "Uncategorized"


def test_validate_handles_empty_reply():
    assert categorizer._validate("") == "Uncategorized"


def test_cache_avoids_second_api_call(monkeypatch):
    monkeypatch.setattr(categorizer, "_cache", {})
    calls = []

    def fake_ask(description):
        calls.append(description)
        return "Food"

    monkeypatch.setattr(categorizer, "_ask_gemini", fake_ask)

    assert categorizer.categorize("Swiggy dinner") == "Food"
    assert categorizer.categorize("swiggy dinner") == "Food"
    assert len(calls) == 1


def test_add_expense_saves_ai_category(client, monkeypatch):
    monkeypatch.setattr(categorizer, "_ask_gemini", lambda description: "Transport")

    response = client.post(
        "/expenses", json={"description": "Uber to college", "amount": 220}
    )

    assert response.status_code == 200
    assert response.json()["category"] == "Transport"
    listed = client.get("/expenses").json()
    assert len(listed) == 1
    assert listed[0]["category"] == "Transport"


def test_ai_failure_falls_back_to_uncategorized(client, monkeypatch):
    monkeypatch.setattr(categorizer, "_ask_gemini", lambda description: "")

    response = client.post("/expenses", json={"description": "Mystery", "amount": 10})

    assert response.status_code == 200
    assert response.json()["category"] == "Uncategorized"


def test_invalid_amount_is_rejected(client):
    response = client.post("/expenses", json={"description": "Tea", "amount": "abc"})

    assert response.status_code == 422