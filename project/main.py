
from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="GRC Compliance Automation API",
    description="API for managing GRC controls, evidence and exceptions",
    version="1.0.0"
)

DATABASE_NAME = r"E:\GRC automation\grc_database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/")
def home():
    return {
        "message": "GRC Compliance Automation API is running!"
    }


@app.get("/controls")
def get_controls():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, control_code, control_description, category
        FROM controls
        ORDER BY id
        """
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


@app.get("/evidence")
def get_evidence():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT control_code, evidence_name, evidence_status,
               evidence_quality, evidence_date, due_date
        FROM evidence
        ORDER BY id
        """
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


@app.get("/exceptions")
def get_exceptions():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT control_code, risk_severity,
               remediation_status, remediation_owner,
               remediation_due_date
        FROM exceptions
        ORDER BY id
        """
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]



@app.get("/dashboard-summary")
def get_dashboard_summary():
    connection = get_connection()

    total_controls = connection.execute(
        "SELECT COUNT(*) FROM controls"
    ).fetchone()[0]

    total_evidence = connection.execute(
        "SELECT COUNT(*) FROM evidence"
    ).fetchone()[0]

    passed_controls = connection.execute(
        """
        SELECT COUNT(*)
        FROM evidence
        WHERE evidence_status = 'Submitted'
          AND evidence_quality = 'Valid'
        """
    ).fetchone()[0]

    failed_controls = total_controls - passed_controls

    total_exceptions = connection.execute(
        "SELECT COUNT(*) FROM exceptions"
    ).fetchone()[0]

    missing_evidence = total_controls - total_evidence

    connection.close()

    return {
        "total_controls": total_controls,
        "passed_controls": passed_controls,
        "failed_controls": failed_controls,
        "total_evidence_records": total_evidence,
        "missing_evidence": missing_evidence,
        "total_exceptions": total_exceptions
    }
