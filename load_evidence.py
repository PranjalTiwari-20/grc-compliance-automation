
import sqlite3
from evidence_register import EVIDENCE_REGISTER

connection = sqlite3.connect("grc_database.db")

for item in EVIDENCE_REGISTER:
    connection.execute(
        """
        INSERT INTO evidence (
            control_code,
            evidence_name,
            evidence_status,
            evidence_quality,
            evidence_date,
            due_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item["control_code"],
            item["evidence_name"],
            item["evidence_status"],
            item["evidence_quality"],
            item["evidence_date"],
            item["due_date"]
        )
    )

connection.commit()

result = connection.execute(
    "SELECT COUNT(*) FROM evidence"
).fetchone()

print("Evidence loaded successfully!")
print("Total evidence records:", result[0])

rows = connection.execute(
    """
    SELECT control_code, evidence_name, evidence_status
    FROM evidence
    ORDER BY id
    """
).fetchall()

for row in rows:
    print(tuple(row))

connection.close()
