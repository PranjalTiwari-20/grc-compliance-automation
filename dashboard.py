
import streamlit as st
import requests
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="GRC Compliance Dashboard",
    page_icon="🛡️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("🛡️ GRC Compliance Dashboard")
st.caption("Control Testing, Evidence and Exception Monitoring")


def fetch_data(endpoint):
    response = requests.get(
        f"{API_URL}/{endpoint}",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def create_excel_report(summary, controls_df, evidence_df, exceptions_df):
    output = BytesIO()

    summary_df = pd.DataFrame(
        list(summary.items()),
        columns=["Metric", "Value"]
    )

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_df.to_excel(
            writer,
            sheet_name="GRC Summary",
            index=False
        )

        controls_df.to_excel(
            writer,
            sheet_name="Control Details",
            index=False
        )

        evidence_df.to_excel(
            writer,
            sheet_name="Evidence",
            index=False
        )

        exceptions_df.to_excel(
            writer,
            sheet_name="Exceptions",
            index=False
        )

    output.seek(0)
    return output.getvalue()


try:
    # Fetch data from FastAPI
    summary = fetch_data("dashboard-summary")
    controls_df = pd.DataFrame(fetch_data("controls"))
    evidence_df = pd.DataFrame(fetch_data("evidence"))
    exceptions_df = pd.DataFrame(fetch_data("exceptions"))

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Controls", summary["total_controls"])
    col2.metric("PASS", summary["passed_controls"])
    col3.metric("FAIL", summary["failed_controls"])
    col4.metric("Exceptions", summary["total_exceptions"])

    st.divider()

    col5, col6 = st.columns(2)
    col5.metric("Evidence Records", summary["total_evidence_records"])
    col6.metric("Missing Evidence", summary["missing_evidence"])

    # Charts
    st.divider()
    st.subheader("📊 Control Overview")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Controls by Category**")
        category_counts = (
            controls_df["category"]
            .value_counts()
            .sort_index()
        )
        st.bar_chart(category_counts)

    with chart_col2:
        st.markdown("**PASS vs FAIL**")
        status_counts = pd.Series({
            "PASS": summary["passed_controls"],
            "FAIL": summary["failed_controls"]
        })
        st.bar_chart(status_counts)

    # Search and filters
    st.divider()
    st.subheader("🔎 Search & Filter Controls")

    search = st.text_input(
        "Search by Control Code or Description"
    )

    categories = sorted(
        controls_df["category"].dropna().unique()
    )

    selected_categories = st.multiselect(
        "Filter by Category",
        options=categories,
        default=categories
    )

    filtered_df = controls_df[
        controls_df["category"].isin(selected_categories)
    ].copy()

    if search:
        matches = (
            filtered_df["control_code"].str.contains(
                search, case=False, na=False
            )
            |
            filtered_df["control_description"].str.contains(
                search, case=False, na=False
            )
        )
        filtered_df = filtered_df[matches]

    st.caption(f"Showing {len(filtered_df)} controls")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Evidence table
    st.divider()
    st.subheader("📁 Evidence Records")

    st.dataframe(
        evidence_df,
        use_container_width=True,
        hide_index=True
    )

    # Exceptions table
    st.divider()
    st.subheader("⚠️ Exceptions & Remediation")

    st.dataframe(
        exceptions_df,
        use_container_width=True,
        hide_index=True
    )

    # Excel download
    st.divider()
    st.subheader("📥 Export GRC Report")

    excel_file = create_excel_report(
        summary,
        controls_df,
        evidence_df,
        exceptions_df
    )

    st.download_button(
        label="Download GRC Excel Report",
        data=excel_file,
        file_name="GRC_Compliance_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

except requests.RequestException:
    st.error(
        "FastAPI is not responding. "
        "Please start the API server first."
    )

except (KeyError, ValueError) as error:
    st.error(f"Could not process API data: {error}")
