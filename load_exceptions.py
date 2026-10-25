
import sqlite3
import pandas as pd

from evidence_register import EVIDENCE_REGISTER

connection = sqlite3.connect("grc_database.db")

# Read the control matrix
controls = pd.read_excel(
    "data/GRC_Control_Matrix_ID_Code_Description.xlsx"
)

# Map evidence records to controls
evidence_map = {
    item["control_code"]: item
    for item in EVIDENCE_REGISTER
}

for _, control in controls.iterrows():
    code = control["Control Code"]
    evidence = evidence_map.get(code)

    # Determine whether the evidence passes validation
    if evidence is None:
        validation_result = "FAIL"
        quality = "Missing"
        status = "Not Submitted"
    else:
        status = evidence["evidence_status"]
        quality = evidence["evidence_quality"]

        if status == "Submitted" and quality == "Valid":
            validation_result = "PASS"
        else:
            validation_result = "FAIL"

    # Store exceptions and remediation for failed controls
    if validation_result == "FAIL":
        if status == "Not Submitted" or quality == "Invalid":
            severity = "High"
        else:
            severity = "Low"

        connection.execute(
            """
            INSERT INTO exceptions (
                control_code,
                risk_severity,
                remediation_status,
                remediation_owner,
                remediation_due_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                code,
                severity,
                "Open",
                "Compliance Team",
                "2026-09-30"
            )
        )

connection.commit()

exception_count = connection.execute(
    "SELECT COUNT(*) FROM exceptions"
).fetchone()[0]

print("Exceptions and remediation records stored!")
print("Total exception records:", exception_count)

rows = connection.execute(
    """
    SELECT control_code, risk_severity,
           remediation_status, remediation_owner
    FROM exceptions
    ORDER BY id
    LIMIT 10
    """
).fetchall()

for row in rows:
    print(tuple(row))

connection.close()
