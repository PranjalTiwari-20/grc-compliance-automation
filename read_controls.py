import pandas as pd
from evidence_requirements import EVIDENCE_REQUIREMENTS
from evidence_register import EVIDENCE_REGISTER


# --------------------------------------------------
# 1. Read control matrix
# --------------------------------------------------

file_path = "data/GRC_Control_Matrix_ID_Code_Description.xlsx"

controls = pd.read_excel(file_path)

print(controls)

print("\nTotal number of controls:", len(controls))


# --------------------------------------------------
# 2. Identify control categories
# --------------------------------------------------

print("\nControls by category:")

categories = controls["Control Code"].str.split("-").str[0]

print(categories.value_counts())

controls["Category"] = categories


# --------------------------------------------------
# 3. Display updated control data
# --------------------------------------------------

print("\nUpdated control data:")

print(controls.head())


# --------------------------------------------------
# 4. Evidence mapping
# --------------------------------------------------

controls["Evidence Required"] = controls["Control Code"].map(
    EVIDENCE_REQUIREMENTS
)


# --------------------------------------------------
# 5. Create GRC tracking fields
# --------------------------------------------------

controls["Evidence Status"] = "Not Submitted"
controls["Evidence Quality"] = "Missing"
controls["Evidence Name"] = ""
controls["Evidence Date"] = ""
controls["Due Date"] = ""
controls["Timeliness"] = "Not Applicable"


# --------------------------------------------------
# 6. Load evidence from Evidence Register
# --------------------------------------------------

for evidence in EVIDENCE_REGISTER:

    control_code = evidence["control_code"]

    controls.loc[
        controls["Control Code"] == control_code,
        "Evidence Status"
    ] = evidence["evidence_status"]

    controls.loc[
        controls["Control Code"] == control_code,
        "Evidence Quality"
    ] = evidence["evidence_quality"]

    controls.loc[
        controls["Control Code"] == control_code,
        "Evidence Name"
    ] = evidence["evidence_name"]

    controls.loc[
        controls["Control Code"] == control_code,
        "Evidence Date"
    ] = evidence["evidence_date"]

    controls.loc[
        controls["Control Code"] == control_code,
        "Due Date"
    ] = evidence["due_date"]


# --------------------------------------------------
# 7. Convert dates
# --------------------------------------------------

controls["Evidence Date"] = pd.to_datetime(
    controls["Evidence Date"],
    errors="coerce"
)

controls["Due Date"] = pd.to_datetime(
    controls["Due Date"],
    errors="coerce"
)


# --------------------------------------------------
# 8. Display submitted evidence
# --------------------------------------------------

print("\nSubmitted Evidence:")

print(
    controls[
        controls["Evidence Status"] == "Submitted"
    ][
        [
            "Control Code",
            "Evidence Name",
            "Evidence Date",
            "Due Date",
            "Evidence Status",
            "Evidence Quality"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 9. Validate evidence
# --------------------------------------------------

def validate_evidence(row):

    if row["Evidence Status"] != "Submitted":
        return "FAIL"

    if row["Evidence Quality"] != "Valid":
        return "FAIL"

    return "PASS"


controls["Validation Result"] = controls.apply(
    validate_evidence,
    axis=1
)


# --------------------------------------------------
# 10. Check evidence timeliness
# --------------------------------------------------

def check_timeliness(row):

    if row["Evidence Status"] != "Submitted":
        return "Not Submitted"

    if pd.isna(row["Evidence Date"]) or pd.isna(row["Due Date"]):
        return "Date Missing"

    if row["Evidence Date"] <= row["Due Date"]:
        return "On Time"

    return "Overdue"


controls["Timeliness"] = controls.apply(
    check_timeliness,
    axis=1
)


# --------------------------------------------------
# 11. Identify exceptions
# --------------------------------------------------

controls["Exception"] = controls["Validation Result"].apply(
    lambda x: "Yes" if x == "FAIL" else "No"
)


# --------------------------------------------------
# 12. Assign risk severity
# --------------------------------------------------

def assign_risk_severity(row):

    if row["Validation Result"] == "PASS":
        return "None"

    if row["Evidence Status"] == "Not Submitted":
        return "High"

    if row["Evidence Quality"] == "Invalid":
        return "High"

    if row["Timeliness"] == "Overdue":
        return "Medium"

    return "Low"


controls["Risk Severity"] = controls.apply(
    assign_risk_severity,
    axis=1
)


# --------------------------------------------------
# 13. Create remediation status
# --------------------------------------------------

controls["Remediation Status"] = controls["Validation Result"].apply(
    lambda x: "Open" if x == "FAIL" else "Not Required"
)


# --------------------------------------------------
# 14. Add remediation owner and due date
# --------------------------------------------------

controls["Remediation Owner"] = ""
controls["Remediation Due Date"] = ""

controls.loc[
    controls["Validation Result"] == "FAIL",
    "Remediation Owner"
] = "Compliance Team"

controls.loc[
    controls["Validation Result"] == "FAIL",
    "Remediation Due Date"
] = "2026-09-30"


# --------------------------------------------------
# 15. GRC Summary Metrics
# --------------------------------------------------

total_controls = len(controls)

pass_count = (
    controls["Validation Result"] == "PASS"
).sum()

fail_count = (
    controls["Validation Result"] == "FAIL"
).sum()

exception_count = (
    controls["Exception"] == "Yes"
).sum()

missing_evidence_count = (
    controls["Evidence Status"] == "Not Submitted"
).sum()

invalid_evidence_count = (
    controls["Evidence Quality"] == "Invalid"
).sum()

overdue_count = (
    controls["Timeliness"] == "Overdue"
).sum()

open_remediation_count = (
    controls["Remediation Status"] == "Open"
).sum()


print("\n========================================")
print("           GRC SUMMARY")
print("========================================")

print("Total Controls:", total_controls)
print("PASS:", pass_count)
print("FAIL:", fail_count)
print("Exceptions:", exception_count)
print("Missing Evidence:", missing_evidence_count)
print("Invalid Evidence:", invalid_evidence_count)
print("Overdue Evidence:", overdue_count)
print("Open Remediations:", open_remediation_count)


# --------------------------------------------------
# 16. Final GRC Results
# --------------------------------------------------

print("\nFinal GRC Results:")

print(
    controls[
        [
            "Control Code",
            "Evidence Required",
            "Evidence Name",
            "Evidence Date",
            "Due Date",
            "Evidence Status",
            "Evidence Quality",
            "Timeliness",
            "Validation Result",
            "Exception",
            "Risk Severity",
            "Remediation Status",
            "Remediation Owner",
            "Remediation Due Date"
        ]
    ].head(50).to_string(index=False)
)


# --------------------------------------------------
# 17. Check controls without evidence requirements
# --------------------------------------------------

print("\nControls without evidence requirements:")

missing_evidence = controls[
    controls["Evidence Required"].isna()
]

print(
    missing_evidence[
        [
            "Control Code",
            "Control Description"
        ]
    ].to_string(index=False)
)

# STEP 16: EXPORT GRC REPORT TO EXCEL

output_file = "GRC_Compliance_Report.xlsx"

# Create summary statistics
summary = pd.DataFrame({
    "Metric": [
        "Total Controls",
        "PASS",
        "FAIL",
        "Exceptions",
        "Missing Evidence",
        "Invalid Evidence",
        "Overdue Evidence",
        "Open Remediations"
    ],
    "Count": [
        total_controls,
        pass_count,
        fail_count,
        exception_count,
        missing_evidence_count,
        invalid_evidence_count,
        overdue_count,
        open_remediation_count
    ]
})

# Export detailed results and summary into separate sheets
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    summary.to_excel(
        writer,
        sheet_name="GRC Summary",
        index=False
    )

    controls.to_excel(
        writer,
        sheet_name="Control Details",
        index=False
    )

print("\nGRC report exported successfully!")
print("File:", output_file)
