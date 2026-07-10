import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./storage/test_leads.db"
os.environ["SMTP_HOST"] = ""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_lead_and_auth_guard() -> None:
    response = client.post(
        "/api/leads",
        data={"first_name": "Ava", "last_name": "Stone", "email": "ava@example.com"},
        files={"resume": ("resume.pdf", b"%PDF-1.4 sample", "application/pdf")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["state"] == "PENDING"
    assert payload["email"] == "ava@example.com"

    assert client.get("/api/leads").status_code == 401


def test_internal_user_can_list_and_update_leads() -> None:
    login = client.post(
        "/api/auth/login",
        json={"username": "attorney@company.com", "password": "change-me"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    leads = client.get("/api/leads", headers=headers)
    assert leads.status_code == 200
    lead_id = leads.json()[0]["id"]

    updated = client.patch(f"/api/leads/{lead_id}", json={"state": "REACHED_OUT"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["state"] == "REACHED_OUT"


def test_email_fallback_writes_outbox() -> None:
    outbox = Path("storage/outbox")
    assert any(outbox.glob("*.eml"))
