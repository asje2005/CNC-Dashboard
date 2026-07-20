# Caregiver Dashboard MVP

A responsive FastAPI and SQLite application for coordinating in-home or clinic-based caregiving. The MVP includes an operational dashboard, seeded sample data, tested endpoints, and an initial domain architecture for patients, caregivers, medications, tasks, appointments, vitals, and notes.

## Features

- **Dashboard homepage** with care summary metrics and responsive card layouts.
- **SQLite persistence** initialized automatically through the FastAPI lifespan hook.
- **Seed data** for three patients, caregivers, medications, tasks, appointments, vitals, and notes.
- **JSON summary API** at `/api/summary` for frontend or integration experiments.
- **Health check** at `/health` for local runtime checks.
- **Mobile-first frontend** built with Jinja templates and plain CSS.
- **Regression tests** for rendering, API responses, health checks, and idempotent database seeding.
- **React Native mobile starter** under `mobile/` with separate Android and iOS entry files for design exploration.

## Project Structure

```text
app/
  main.py                 FastAPI app, lifespan startup, dashboard route, API endpoints
  models.py               SQLite schema, connection helpers, and sample-data seeding
  data/                   Runtime SQLite database location (created automatically)
  templates/
    dashboard.html        Responsive dashboard homepage
  static/
    css/styles.css        Frontend styling and responsive breakpoints
mobile/
  App.js                 Default Expo React Native entry point
  App.android.jsx        Android React Native entry point
  App.ios.jsx            iOS React Native entry point
  src/                   Shared mobile screen, components, sample data, and theme tokens
tests/
  test_app.py             Application and database regression tests
scripts/
  monitor.py              Legacy CNC log watcher retained from the original repo
requirements.txt          Python dependencies
README.md                 Project documentation
```

## Data Model

The initial architecture creates these SQLite tables:

| Table | Purpose |
| --- | --- |
| `patients` | Demographics, contact details, care level, condition, emergency contact |
| `caregivers` | Care team members, roles, contact information, shifts |
| `medications` | Patient medication schedule, due status, and instructions |
| `tasks` | Care tasks assigned to patients and optional caregivers |
| `appointments` | Provider visits, locations, appointment times, and transportation notes |
| `vitals` | Recent clinical readings such as heart rate, blood pressure, temperature, oxygen |
| `notes` | Timestamped caregiver notes by category |

Relationships use foreign keys from care records back to `patients`, with optional assignments to `caregivers` for tasks and notes.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000> in a desktop or mobile browser. The database is created at `app/data/caregiver.db` on first startup.

## API

- `GET /` renders the dashboard homepage.
- `GET /api/summary` returns patients, tasks, medications, appointments, vitals, and notes as JSON.
- `GET /health` returns `{ "status": "ok" }`.

## Mobile Prototype

The `mobile/` folder contains an Expo React Native starter app with `App.android.jsx` and `App.ios.jsx` entry files. Start there when you want to experiment with native mobile UI patterns separately from the working FastAPI dashboard. See `mobile/README.md` for setup notes.

```bash
cd mobile
npm install
npm run android
npm run ios
```

## Testing

```bash
pytest
python -m compileall app tests
```

## Development Notes

- Delete `app/data/caregiver.db` to regenerate the seeded sample data.
- The frontend uses no build step; update `app/templates/dashboard.html` and `app/static/css/styles.css` directly.
- Sample dates are fixed to July 2026 so tests and screenshots are deterministic.
- This is an MVP and does not yet include authentication, audit trails, form-based CRUD, or production-grade medical compliance controls.
