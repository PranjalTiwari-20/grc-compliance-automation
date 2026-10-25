
import sqlite3

connection = sqlite3.connect("grc_database.db")

tables = {
    "controls": "Controls",
    "evidence": "Evidence",
    "exceptions": "Exceptions"
}

print("===== GRC DATABASE VERIFICATION =====")

for table, label in tables.items():
    count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{label}: {count}")

print("\nSample Exceptions:")

rows = connection.execute("""
    SELECT control_code, risk_severity, remediation_status
    FROM exceptions
    ORDER BY id
    LIMIT 5
""").fetchall()

for row in rows:
    print(tuple(row))

connection.close()
