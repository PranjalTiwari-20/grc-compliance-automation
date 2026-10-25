
import sqlite3

DATABASE_NAME = "grc_database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controls (
            id INTEGER PRIMARY KEY,
            control_code TEXT UNIQUE NOT NULL,
            control_description TEXT NOT NULL,
            category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_code TEXT NOT NULL,
            evidence_name TEXT,
            evidence_status TEXT,
            evidence_quality TEXT,
            evidence_date TEXT,
            due_date TEXT,
            FOREIGN KEY (control_code)
                REFERENCES controls(control_code)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exceptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_code TEXT NOT NULL,
            risk_severity TEXT,
            remediation_status TEXT,
            remediation_owner TEXT,
            remediation_due_date TEXT,
            FOREIGN KEY (control_code)
                REFERENCES controls(control_code)
        )
    """)

    connection.commit()
    connection.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
