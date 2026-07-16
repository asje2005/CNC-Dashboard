from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.models import initialize_database


def test_dashboard_homepage_renders_sections() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Caregiver Dashboard" in response.text
    assert "Patients" in response.text
    assert "Medications" in response.text
    assert "Recent Notes" in response.text


def test_summary_api_returns_all_domain_collections() -> None:
    with TestClient(app) as client:
        response = client.get("/api/summary")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {"patients", "tasks", "medications", "appointments", "vitals", "notes"}
    assert len(payload["patients"]) == 3
    assert payload["tasks"][0]["patient_name"]


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_initialization_is_idempotent(tmp_path: Path) -> None:
    database_path = tmp_path / "caregiver.db"

    initialize_database(database_path)
    initialize_database(database_path)

    with sqlite3.connect(database_path) as conn:
        patient_count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        caregiver_count = conn.execute("SELECT COUNT(*) FROM caregivers").fetchone()[0]
        task_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    assert patient_count == 3
    assert caregiver_count == 3
    assert task_count == 4
