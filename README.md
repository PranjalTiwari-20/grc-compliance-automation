# GRC Compliance Automation Platform

**A Python-based platform for organizing compliance controls, tracking evidence records, evaluating control status, and monitoring remediation activities.**

Built with Python, FastAPI, SQLite, Streamlit, and n8n.

---

## 1. Project Overview

Governance, Risk, and Compliance (GRC) teams work with multiple compliance controls, evidence records, audit requirements, exceptions, and remediation activities.

Managing these activities manually across spreadsheets and different tools can make it difficult to maintain visibility into control status, identify missing information, and track outstanding issues.

The GRC Compliance Automation Platform is a project designed to bring these activities into a centralized workflow.

It combines a Python-based backend, a relational database, a REST API, an interactive dashboard, and workflow automation to demonstrate how compliance data can be organized and processed programmatically.

The platform currently supports retrieving compliance controls, evidence records, and exceptions; evaluating control records using predefined rules; summarizing compliance results; and identifying potentially overdue remediation items.

The project is intended as a foundation for developing more advanced GRC automation capabilities.

## 2. Problem Statement

Traditional compliance workflows often involve repetitive activities such as:

- Maintaining compliance control inventories.
- Organizing evidence records associated with compliance activities.
- Reviewing whether evidence information is available.
- Tracking compliance exceptions and remediation deadlines.
- Calculating control status and preparing compliance summaries.
- Identifying open issues that require follow-up.
- Consolidating information for internal reviews and reporting.

These activities can become difficult to manage when information is spread across multiple spreadsheets or systems.

### Our Approach

This project demonstrates how these activities can be supported through a centralized, programmatic workflow.

Instead of relying entirely on manual data review, the platform retrieves structured records through APIs, applies predefined evaluation rules, summarizes the resulting status, and presents compliance information through a dashboard.

**Important:** Automated status evaluation helps organize compliance reviews, but it does not independently prove that a control is effective or that its evidence satisfies an auditor's requirements.

## 3. Key Features

### 3.1 Compliance Control Management

The platform maintains a structured inventory of compliance controls.

Each control represents a requirement that an organization may need to implement, monitor, or assess.

The project includes a control matrix containing control identifiers, control codes, and control descriptions.

The controls endpoint allows the application and connected workflows to retrieve these records programmatically.

**Why it matters:** A centralized control inventory provides a foundation for mapping compliance requirements to evidence, tracking assessment results, and identifying outstanding work.

### 3.2 Evidence Register

The evidence register stores structured records associated with compliance activities.

Evidence records may represent information collected during a compliance review, such as a configuration record, an access review, or a relevant system report.

The current implementation exposes the available evidence records through an API endpoint.

**Why it matters:** A structured register makes evidence information easier to retrieve and process. A future enhancement could connect individual evidence records to specific controls and validate their completeness, relevance, and audit-period coverage.

The current implementation does not automatically verify the authenticity or effectiveness of uploaded evidence.

### 3.3 Control Compliance Evaluation

The platform includes a Python-based evaluation workflow that applies predefined rules to control and evidence records.

The workflow produces a status for each evaluated control, using categories such as:

- **PASS:** The control satisfies the configured evaluation rule.
- **FAIL:** The available records trigger a configured failure condition.
- **Missing Evidence:** The records do not satisfy the configured evidence-availability condition.

The results are then aggregated to produce a compliance summary.

**Why it matters:** Programmatic evaluation can reduce repetitive status calculations and provide a consistent starting point for compliance reviews.

The resulting status is rule-based and should not be interpreted as an independent audit conclusion. The quality of the result depends on the completeness of the data and the accuracy of the evaluation logic.

### 3.4 Exception and Remediation Tracking

The platform retrieves compliance exceptions and processes their remediation-related fields.

The remediation workflow summarizes exception information, including open items and severity classifications where those fields are available.

A separate overdue-remediation check identifies open exceptions whose due dates meet the configured overdue condition.

**Why it matters:** Tracking exceptions in a structured format helps compliance teams identify unresolved issues and prioritize follow-up activities.

The current implementation identifies potentially overdue items; it does not automatically remediate them or notify responsible employees.

### 3.5 REST API

The backend uses FastAPI to expose compliance data through HTTP endpoints.

This separates data retrieval from the dashboard and automation workflow, allowing multiple components to access the same underlying information.

Available endpoints include:

| Endpoint | Purpose |
|---|---|
| `GET /` | Check whether the API is running |
| `GET /controls` | Retrieve compliance control records |
| `GET /evidence` | Retrieve evidence records |
| `GET /exceptions` | Retrieve compliance exceptions |
| `GET /dashboard-summary` | Retrieve dashboard summary information |

FastAPI also provides interactive API documentation at `/docs` when the application is running.

**Why it matters:** An API-based architecture provides a foundation for integrating additional dashboards, automation workflows, and other authorized systems in the future.

### 3.6 Interactive Compliance Dashboard

The project uses Streamlit to provide a dashboard for reviewing compliance information.

The dashboard brings together information such as:

- Compliance summary metrics.
- Control records.
- Evidence records.
- Exception records.
- Visual summaries and charts.
- Search and category filters.
- A downloadable compliance report.

**Why it matters:** A dashboard makes structured compliance data easier to review without requiring users to query the database manually.

The dashboard presents information available in the underlying application; it does not independently validate control effectiveness.

### 3.7 Workflow Automation with n8n

The project includes an n8n workflow that connects to the FastAPI endpoints through HTTP Request nodes.

The workflow retrieves control, evidence, exception, and dashboard-summary data. A Merge node combines the retrieved records, after which Code nodes perform control evaluation and compliance summarization.

Separate workflow branches process remediation information and identify overdue exceptions.

The workflow currently uses a manual trigger, so a user initiates execution from the n8n editor.

**Why it matters:** n8n provides a visual way to orchestrate API calls and processing steps without implementing every workflow connection from scratch.

Future enhancements could include scheduled execution, notifications, and additional integrations, subject to appropriate access permissions.

---

## 4. Technology Stack Explained

| Technology | Role in the Project | Why It Is Used |
|---|---|---|
| Python | Core application logic | Implements data processing, evaluation rules, and remediation checks. |
| FastAPI | Backend REST API | Exposes compliance records through structured HTTP endpoints. |
| SQLite | Database | Stores structured application records in a local relational database. |
| Streamlit | Dashboard | Displays compliance data, metrics, charts, filters, and report downloads. |
| Pandas | Data processing | Supports tabular data manipulation and analysis where used. |
| n8n | Workflow orchestration | Connects API requests and coordinates compliance-processing steps. |
| Excel | Compliance data source and reporting | Supports control matrix management and downloadable reporting. |
| Git | Version control | Tracks source-code changes. |
| GitHub | Repository hosting | Stores the project source code and documents its development. |

### How the Technologies Work Together

**Python** implements the application logic.

**SQLite** provides local storage for the application's structured records.

**FastAPI** makes those records available through API endpoints.

**n8n** calls the endpoints and coordinates the configured evaluation workflow.

**Streamlit** provides a user-facing interface for exploring compliance information and downloading the report.

**Git and GitHub** support source-code version control and project sharing.

Together, these components demonstrate a modular approach to building a basic compliance automation application.

---

## 5. System Architecture

```text
       Compliance Control Matrix
                  |
                  v
          Python Data Loaders
                  |
                  v
            SQLite Database
                  |
                  v
             FastAPI Backend
                  |
        +---------+----------+
        |         |          |
        v         v          v
     Controls  Evidence   Exceptions
        |         |          |
        +---------+----------+
                  |
                  v
            n8n Workflow
                  |
        +---------+----------+
        |                    |
        v                    v
 Control Evaluation   Remediation Checks
        |                    |
        v                    v
 Compliance Summary   Overdue Items
        |                    |
        +---------+----------+
                  |
                  v
         Streamlit Dashboard
                  |
                  v
          Compliance Report
```

*This diagram represents the logical flow of the current prototype. The dashboard also reads the application's data directly through its configured data-access logic.*

---

## 6. Data Flow

The platform follows a sequence of data preparation, retrieval, processing, and presentation.

### Step 1: Prepare Compliance Data

The project includes scripts for reading control information and loading controls, evidence records, and exceptions into the application's database.

### Step 2: Store Structured Records

SQLite provides a local database for the application.

Keeping records in a structured database makes them easier to query and process than maintaining all application data exclusively in separate spreadsheets.

### Step 3: Expose Data Through APIs

FastAPI provides endpoints for retrieving controls, evidence records, exceptions, and dashboard summary information.

### Step 4: Execute the Automation Workflow

The n8n workflow sends HTTP requests to the API and processes the returned records using configured workflow nodes.

### Step 5: Evaluate Compliance Status

The control evaluation logic applies predefined rules and produces control-level statuses.

A separate code node aggregates the evaluation results into a compliance summary.

### Step 6: Monitor Remediation

The remediation workflow processes exception records and identifies open exceptions that meet the configured overdue criteria.

### Step 7: Review Results

The Streamlit dashboard presents compliance information in tables and charts and provides a report-download option.

---

## 7. Project Structure

```text
grc-compliance-automation/
|
|-- data/
|   |-- GRC_Control_Matrix_ID_Code_Description.xlsx
|
|-- project/
|   |-- main.py
|
|-- dashboard.py
|-- database.py
|-- evidence_register.py
|-- evidence_requirements.py
|-- load_controls.py
|-- load_evidence.py
|-- load_exceptions.py
|-- read_controls.py
|-- verify_database.py
|-- n8n_workflow.json
|-- .gitignore
|-- README.md
```

### Important Files

| File | Responsibility |
|---|---|
| `project/main.py` | Defines the FastAPI application and API endpoints. |
| `database.py` | Contains database-related functionality. |
| `dashboard.py` | Implements the Streamlit dashboard. |
| `read_controls.py` | Reads the control matrix. |
| `load_controls.py` | Loads control records into the database. |
| `load_evidence.py` | Loads evidence records. |
| `load_exceptions.py` | Loads exception records. |
| `evidence_register.py` | Supports evidence-register functionality. |
| `evidence_requirements.py` | Contains evidence-requirement-related logic. |
| `verify_database.py` | Supports database verification. |
| `n8n_workflow.json` | Stores the exported n8n workflow configuration. |

---

## 8. Getting Started

### Prerequisites

- Python installed on your system.
- Git installed on your system.
- n8n installed if you want to run the workflow automation.

### 8.1 Clone the Repository

```bash
git clone https://github.com/PranjalTiwari-20/grc-compliance-automation.git
cd grc-compliance-automation
```

### 8.2 Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 8.3 Install Dependencies

If the project includes a maintained `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by the current application:

```bash
pip install fastapi uvicorn streamlit pandas openpyxl
```

Additional dependencies may be required depending on the imports used by the application.

### 8.4 Start the API

From the repository root:

```powershell
cd project
python -m uvicorn main:app --reload
```

The API should be available at:

- API root: `http://127.0.0.1:8000`
- Interactive documentation: `http://127.0.0.1:8000/docs`

Keep the API terminal running while using components that call the API.

### 8.5 Start the Dashboard

Open another terminal in the repository root, activate the virtual environment, and run:

```powershell
python -m streamlit run dashboard.py
```

### 8.6 Run n8n

If n8n is installed, open a separate terminal and run:

```bash
n8n
```

Open `http://localhost:5678` and import `n8n_workflow.json`.

Ensure the FastAPI application is running before executing workflows that call its endpoints.

The workflow currently uses local API URLs, so it is configured for local development rather than direct execution on a remote server.

---

## 9. Current Implementation and Limitations

This project is a working prototype, not a production-ready GRC platform.

The current implementation includes API endpoints, database-backed records, a dashboard, and an n8n workflow for compliance evaluation and remediation checks.

The following limitations should be considered:

- Compliance statuses depend on predefined rules and available data.
- The presence of an evidence record does not prove that a control is effective.
- Evidence authenticity, relevance, and audit-period coverage are not fully validated automatically.
- Remediation monitoring depends on the fields and dates present in the underlying records.
- The n8n workflow uses a manual trigger.
- The application is not currently integrated with Vanta or another external GRC platform.
- Authentication, role-based authorization, production deployment, and comprehensive security controls would be needed before handling real organizational compliance data.

---

## 10. Future Enhancements

Potential improvements include:

- Automated evidence-to-control mapping.
- Evidence completeness and audit-period validation.
- Configurable control evaluation rules.
- Improved exception prioritization and remediation tracking.
- Scheduled n8n workflow execution.
- Notifications for overdue remediation items.
- Automated report generation and distribution.
- Authentication and role-based access control.
- Comprehensive testing and error handling.
- Integration with authorized external GRC and cloud services.
- Deployment with appropriate security and operational monitoring.

---

## 11. Security and Data Handling

This repository should not contain confidential client information, real audit records, credentials, API tokens, or sensitive reports.

Before sharing the project publicly, review the control matrix and all other included files to ensure that they contain only information approved for publication.

Use synthetic or appropriately sanitized data for demonstrations.

---

## 12. Author

**Pranjal Tiwari**

GitHub: https://github.com/PranjalTiwari-20

---

*Developed as a GRC compliance automation portfolio project.*
