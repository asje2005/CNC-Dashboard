from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import fetch_all, fetch_one, initialize_database, rows_to_dicts


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    initialize_database()
    yield


app = FastAPI(title="Caregiver Dashboard", version="0.2.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
templates.env.cache = None


DASHBOARD_QUERIES = {
    "patients": "SELECT * FROM patients ORDER BY last_name, first_name",
    "tasks": """
        SELECT tasks.*, patients.first_name || ' ' || patients.last_name AS patient_name,
               caregivers.first_name || ' ' || caregivers.last_name AS caregiver_name
        FROM tasks
        JOIN patients ON patients.id = tasks.patient_id
        LEFT JOIN caregivers ON caregivers.id = tasks.caregiver_id
        ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, due_at
    """,
    "medications": """
        SELECT medications.*, patients.first_name || ' ' || patients.last_name AS patient_name
        FROM medications
        JOIN patients ON patients.id = medications.patient_id
        ORDER BY CASE medications.status WHEN 'Due soon' THEN 1 WHEN 'Scheduled' THEN 2 ELSE 3 END, next_due
    """,
    "appointments": """
        SELECT appointments.*, patients.first_name || ' ' || patients.last_name AS patient_name
        FROM appointments
        JOIN patients ON patients.id = appointments.patient_id
        ORDER BY starts_at
    """,
    "vitals": """
        SELECT vitals.*, patients.first_name || ' ' || patients.last_name AS patient_name
        FROM vitals
        JOIN patients ON patients.id = vitals.patient_id
        ORDER BY vitals.recorded_at DESC
    """,
    "notes": """
        SELECT notes.*, patients.first_name || ' ' || patients.last_name AS patient_name,
               caregivers.first_name || ' ' || caregivers.last_name AS caregiver_name
        FROM notes
        JOIN patients ON patients.id = notes.patient_id
        LEFT JOIN caregivers ON caregivers.id = notes.caregiver_id
        ORDER BY notes.created_at DESC
    """,
}


def get_dashboard_context(request: Request) -> dict[str, object]:
    open_tasks = fetch_one("SELECT COUNT(*) AS total FROM tasks WHERE status != 'Done'")
    medications_due = fetch_one("SELECT COUNT(*) AS total FROM medications WHERE status = 'Due soon'")
    appointments = fetch_one("SELECT COUNT(*) AS total FROM appointments")
    high_priority = fetch_one("SELECT COUNT(*) AS total FROM tasks WHERE priority = 'High'")
    patients = fetch_one("SELECT COUNT(*) AS total FROM patients")

    return {
        "request": request,
        "stats": {
            "patients": patients["total"] if patients else 0,
            "open_tasks": open_tasks["total"] if open_tasks else 0,
            "medications_due": medications_due["total"] if medications_due else 0,
            "appointments": appointments["total"] if appointments else 0,
            "high_priority": high_priority["total"] if high_priority else 0,
        },
        **{name: fetch_all(query) for name, query in DASHBOARD_QUERIES.items()},
    }


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "dashboard.html", get_dashboard_context(request))


@app.get("/api/summary")
def api_summary() -> dict[str, object]:
    return {name: rows_to_dicts(fetch_all(query)) for name, query in DASHBOARD_QUERIES.items()}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
