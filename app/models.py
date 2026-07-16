from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable

DATABASE_PATH = Path(__file__).resolve().parent / "data" / "caregiver.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    care_level TEXT NOT NULL CHECK (care_level IN ('Low', 'Medium', 'High')),
    primary_condition TEXT,
    emergency_contact TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS caregivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    shift TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT NOT NULL,
    next_due TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Scheduled',
    instructions TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    caregiver_id INTEGER,
    title TEXT NOT NULL,
    due_at TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High')),
    status TEXT NOT NULL DEFAULT 'Open' CHECK (status IN ('Open', 'In progress', 'Done')),
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY(caregiver_id) REFERENCES caregivers(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    provider TEXT NOT NULL,
    location TEXT,
    starts_at TEXT NOT NULL,
    transportation TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,
    heart_rate INTEGER,
    systolic INTEGER,
    diastolic INTEGER,
    temperature REAL,
    oxygen INTEGER,
    notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    caregiver_id INTEGER,
    created_at TEXT NOT NULL,
    category TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY(caregiver_id) REFERENCES caregivers(id) ON DELETE SET NULL
);
"""

PATIENTS = [
    (
        "Martha",
        "Ellis",
        "1942-03-14",
        "555-0142",
        "120 Maple St",
        "High",
        "Type 2 diabetes",
        "Nina Ellis · 555-0199",
    ),
    (
        "Robert",
        "King",
        "1938-11-02",
        "555-0138",
        "45 Cedar Ave",
        "Medium",
        "Hypertension",
        "Sam King · 555-0120",
    ),
    (
        "Aisha",
        "Patel",
        "1950-07-26",
        "555-0150",
        "8 Garden Way",
        "Low",
        "Post-op mobility",
        "Dev Patel · 555-0117",
    ),
]

CAREGIVERS = [
    ("Jamie", "Rivera", "RN", "555-0101", "jamie@example.com", "7 AM - 3 PM"),
    ("Morgan", "Lee", "Home Health Aide", "555-0102", "morgan@example.com", "3 PM - 11 PM"),
    ("Taylor", "Brooks", "Care Coordinator", "555-0103", "taylor@example.com", "On call"),
]

MEDICATIONS = [
    (1, "Metformin", "500 mg", "Twice daily", "2026-07-15 20:00", "Due soon", "Take with dinner."),
    (1, "Lisinopril", "10 mg", "Daily", "2026-07-16 08:00", "Scheduled", "Monitor blood pressure."),
    (2, "Amlodipine", "5 mg", "Daily", "2026-07-15 18:00", "Due soon", "Give with water."),
    (3, "Acetaminophen", "325 mg", "As needed", "PRN", "PRN", "Do not exceed daily maximum."),
]

TASKS = [
    (1, 1, "Check blood glucose", "2026-07-15 17:30", "High", "Open"),
    (2, 2, "Evening walk", "2026-07-15 18:30", "Medium", "Open"),
    (3, 1, "Change dressing", "2026-07-16 09:00", "High", "Open"),
    (1, 3, "Confirm endocrinology referral", "2026-07-17 12:00", "Medium", "In progress"),
]

APPOINTMENTS = [
    (1, "Diabetes follow-up", "Dr. Chen", "North Clinic", "2026-07-15 10:00", "Family transport"),
    (2, "Cardiology check", "Dr. Moore", "Heart Center", "2026-07-17 14:30", "Rideshare"),
    (3, "Physical therapy", "Peak PT", "In home", "2026-07-16 11:00", "Not required"),
]

VITALS = [
    (1, "2026-07-15 16:00", 78, 128, 76, 98.4, 97, "Glucose 142 mg/dL"),
    (2, "2026-07-15 15:45", 72, 136, 82, 98.1, 96, "Mild ankle swelling"),
    (3, "2026-07-15 14:15", 84, 122, 74, 99.0, 98, "Pain 3/10"),
]

NOTES = [
    (1, 1, "2026-07-15 16:20", "Observation", "Patient ate full lunch and tolerated medication well."),
    (2, 2, "2026-07-15 15:55", "Family", "Daughter requested update after cardiology appointment."),
    (3, 1, "2026-07-15 14:30", "Mobility", "Completed transfer from bed to chair with minimal assistance."),
]


def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def insert_many(conn: sqlite3.Connection, query: str, rows: Iterable[tuple[Any, ...]]) -> None:
    conn.executemany(query, rows)


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as conn:
        conn.executescript(SCHEMA)
        existing = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        if existing:
            return

        insert_many(
            conn,
            """
            INSERT INTO patients (
                first_name, last_name, date_of_birth, phone, address,
                care_level, primary_condition, emergency_contact
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            PATIENTS,
        )
        insert_many(
            conn,
            """
            INSERT INTO caregivers (first_name, last_name, role, phone, email, shift)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            CAREGIVERS,
        )
        insert_many(
            conn,
            """
            INSERT INTO medications (
                patient_id, name, dosage, frequency, next_due, status, instructions
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            MEDICATIONS,
        )
        insert_many(
            conn,
            """
            INSERT INTO tasks (patient_id, caregiver_id, title, due_at, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            TASKS,
        )
        insert_many(
            conn,
            """
            INSERT INTO appointments (
                patient_id, title, provider, location, starts_at, transportation
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            APPOINTMENTS,
        )
        insert_many(
            conn,
            """
            INSERT INTO vitals (
                patient_id, recorded_at, heart_rate, systolic, diastolic,
                temperature, oxygen, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            VITALS,
        )
        insert_many(
            conn,
            """
            INSERT INTO notes (patient_id, caregiver_id, created_at, category, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            NOTES,
        )


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def fetch_one(query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(query, params).fetchone()
