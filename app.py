import streamlit as st
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Initialize Faker
fake = Faker()

# --- Data Generation Functions (Enhanced) ---
def generate_fi_documents(n=200):
    plants = [f"PLANT_{i:03d}" for i in range(1, 5)]
    doc_types = ["Invoice", "Credit Memo", "Payment", "Journal Entry"]
    data = []
    for _ in range(n):
        doc = {
            "DOCUMENT_NUMBER": fake.unique.random_number(digits=8),
            "PLANT": random.choice(plants),
            "POSTING_DATE": fake.date_between(start_date="-2y", end_date="today"),
            "DOCUMENT_TYPE": random.choice(doc_types),
            "AMOUNT": round(random.uniform(1000, 100000), 2),
            "APPROVER": fake.name(),
            "PROCESS_TIME_DAYS": random.randint(1, 10),
        }
        data.append(doc)
    return pd.DataFrame(data)

def generate_audit_findings(n=80):
    plants = [f"PLANT_{i:03d}" for i in range(1, 5)]
    risk_categories = ["Financial", "Operational", "Compliance", "Cybersecurity"]
    statuses = ["Open", "In Progress", "Remediated", "Recurring"]
    data = []
    for _ in range(n):
        finding = {
            "FINDING_ID": fake.unique.random_number(digits=6),
            "PLANT": random.choice(plants),
            "RISK_CATEGORY": random.choice(risk_categories),
            "STATUS": random.choice(statuses),
            "SEVERITY": random.choice(["Low", "Medium", "High", "Critical"]),
            "REMEDIATION_DATE": fake.date_between(start_date="today", end_date="+90d"),
            "ESTIMATED_IMPACT_USD": round(random.uniform(5000, 500000), 2),
            "AUDIT_CYCLE_TIME_DAYS": random.randint(5, 45),
        }
        data.append(finding)
    return pd.DataFrame(data)

def generate_control_testing(n=50):
    plants = [f"PLANT_{i:03d}" for i in range(1, 5)]
    control_types = ["Preventive", "Detective", "Corrective", "Automated"]
    data = []
    for _ in range(n):
        test = {
            "CONTROL_ID": fake.unique.random_number(digits=5),
            "PLANT": random.choice(plants),
            "CONTROL_TYPE": random.choice(control_types),
            "TEST_DATE": fake.date_between(start_date="-1y", end_date="today"),
            "RESULT": random.choice(["Pass", "Fail", "Partial"]),
            "REMEDIATION_STATUS": random.choice(["Not Started", "In Progress", "Completed", "Overdue"]),
            "COST_PER_TEST_USD": round(random.uniform(100, 5000), 2),
        }
        data.append(test)
    return pd.DataFrame(data)

def generate_anomalies(n=40):
    plants = [f"PLANT_{i:03d}" for i in range(1, 5)]
    anomaly_types = ["Duplicate", "Missing", "Outlier", "Unauthorized", "Late"]
    statuses = ["Investigating", "Confirmed", "False Positive", "Resolved"]
    data = []
    for _ in range(n):
        anomaly = {
            "TRANSACTION_ID": fake.unique.random_number(digits=7),
            "PLANT": random.choice(plants),
            "TYPE": random.choice(anomaly_types),
            "STATUS": random.choice(statuses),
            "DETECTION_DATE": fake.date_between(start_date="-6m", end_date="today"),
            "RESOLUTION_TIME_DAYS": random.randint(1, 30) if random.choice([True, False]) else None,
        }
        data.append(anomaly)
    return pd.DataFrame(data)

def generate_sox_controls(n=30):
    plants = [f"PLANT_{i:03d}" for i in range(1, 5)]
    data = []
    for _ in range(n):
        sox = {
            "CONTROL_ID": fake.unique.random_number(digits=4),
            "PLANT": random.choice(plants),
            "TEST_DATE": fake.date_between(start_date="-1y", end_date="today"),
            "RESULT": random.choice(["Pass", "Fail", "Not Tested"]),
            "GAP_DESCRIPTION": fake.sentence() if random.choice([True, False]) else None,
            "REMEDIATION_COST_USD": round(random.uniform(1000, 100000), 2) if random.choice([True, False]) else None,
            "OWNER": fake.name(),
        }
        data.append(sox)
    return pd.DataFrame(data)

def generate_etl_metrics(n=20):
    systems = ["SAP", "Oracle", "EPICOR"]
    data = []
    for _ in range(n):
        etl = {
            "ETL_JOB_ID": fake.unique.random_number(digits=5),
            "SYSTEM": random.choice(systems),
            "JOB_DATE": fake.date_between(start_date="-1y", end_date="today"),
            "STATUS": random.choice(["Success", "Failed", "Partial"]),
            "ERROR_COUNT": random.randint(0, 20),
            "PROCESSING_TIME_MIN": random.randint(5, 120),
        }
        data.append(etl)
    return pd.DataFrame(data)

# --- Generate Data ---
fi_documents = generate_fi_documents()
audit_findings = generate_audit_findings()
control_testing = generate_control_testing()
anomalies = generate_anomalies()
sox_controls = generate_sox_controls()
etl_metrics = generate_etl_metrics()

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="ITT Inc. Audit Dashboard", page_icon="📊")
st.title("ITT Inc. Internal Audit Analytics Dashboard")
st.markdown("**CxO-Level Insights for Global Plants (Aerospace, Transportation, Energy, Industrial)**")

# Sidebar Filters
st.sidebar.header("Filters")
plant_filter = st.sidebar.selectbox("Select Plant", ["All"] + [f"PLANT_{i:03d}" for i in range(1, 5)])
time_period = st.sidebar.select_slider(
    "Select Time Period (Months)",
    options=["1M", "3M", "6M", "1Y", "2Y"],
    value="6M"
)
risk_category = st.sidebar.multiselect(
    "Select Risk Category",
    ["Financial", "Operational", "Compliance", "Cybersecurity"],
    default=["Financial", "Operational"]
)

# Filter data based on sidebar
if plant_filter != "All":
    fi_documents = fi_documents[fi_documents["PLANT"] == plant_filter]
    audit_findings = audit_findings[audit_findings["PLANT"] == plant_filter]
    control_testing = control_testing[control_testing["PLANT"] == plant_filter]
    anomalies = anomalies[anomalies["PLANT"] == plant_filter]
    sox_controls = sox_controls[sox_controls["PLANT"] == plant_filter]

if time_period:
    months = int(time_period.replace("M", "")) if "M" in time_period else int(time_period.replace("Y", "")) * 12
    cutoff_date = datetime.now() - timedelta(days=30 * months)
    fi_documents = fi_documents[pd.to_datetime(fi_documents["POSTING_DATE"]) >= cutoff_date]
    audit_findings = audit_findings[pd.to_datetime(audit_findings["REMEDIATION_DATE"]) >= cutoff_date]
    control_testing = control_testing[pd.to_datetime(control_testing["TEST_DATE"]) >= cutoff_date]
    anomalies = anomalies[pd.to_datetime(anomalies["DETECTION_DATE"]) >= cutoff_date]
    sox_controls = sox_controls[pd.to_datetime(sox_controls["TEST_DATE"]) >= cutoff_date]

if risk_category:
    audit_findings = audit_findings[audit_findings["RISK_CATEGORY"].isin(risk_category)]

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Summary",
    "Risk & Control Dashboard",
    "Anomaly & Exception",
    "SOX Compliance",
    "Data Quality & ETL",
    "Automation & Scripts"
])

# --- Executive Summary Tab (Enhanced) ---
with tab1:
    st.header("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Audit Health Score", "87/100", "+5% YoY")
    with col2:
        st.metric("High-Risk Findings", audit_findings[audit_findings["SEVERITY"] == "High"].shape[0], "-12% YoY")
    with col3:
        st.metric("Control Effectiveness", "92%", "+3% QoQ")
    with col4:
        st.metric("Cost per Audit (USD)", f"{round(control_testing['COST_PER_TEST_USD'].mean(), 2)}", "-8% YoY")

    st.subheader("Strategic Business Suggestions")
    st.markdown(
        """
        1. **Adopt Predictive Analytics:**
           - Use machine learning to predict high-risk transactions in **SAP FI/CO modules** (e.g., duplicate payments, unauthorized journal entries).
           - *Potential Value:* Reduce financial loss by **20%** in 12 months.

        2. **Integrate ERP Systems:**
           - Break down silos between **SAP, Oracle, and EPICOR** with a unified data lake.
           - *Potential Value:* Improve data accuracy by **25%** and reduce ETL errors by **30%**.

        3. **Automate SOX Testing:**
           - Deploy **Python-based CAATs** for 100% of SOX controls in **Plant 1 & Plant 2** (highest risk exposure).
           - *Potential Value:* Save **$250K/year** in manual testing costs.

        4. **Enhance Cybersecurity Audits:**
           - Expand audit scope to include **OT (Operational Technology) systems** in energy/industrial plants.
           - *Potential Value:* Mitigate **$1M+** in potential cyber incident costs.

        5. **Risk-Based Audit Planning:**
           - Allocate **70% of audit resources** to high-severity findings (e.g., Financial > Compliance).
           - *Potential Value:* Increase risk coverage by **40%**.
        """
    )

    st.subheader("Next Steps & Ownership")
    st.dataframe(pd.DataFrame({
        "Action Item": [
            "Deploy predictive analytics for SAP FI/CO",
            "Unify ERP data into a single lake",
            "Automate SOX testing for Plants 1 & 2",
            "Conduct OT cybersecurity audits",
            "Reallocate audit resources to high-severity risks",
        ],
        "Owner": [
            "Director of Data Science",
            "IT Director",
            "Chief Audit Executive (CAE)",
            "CISO",
            "CAE",
        ],
        "Timeline": [
            "Q3 2026",
            "Q4 2026",
            "Q1 2027",
            "Q2 2027",
            "Ongoing",
        ],
        "Business Value": [
            "$500K/year savings",
            "$150K/year efficiency gain",
            "$250K/year cost reduction",
            "$1M+ risk mitigation",
            "40% improved risk coverage",
        ],
    }))

    st.subheader("Key Challenges & Mitigation")
    st.markdown(
        """
        | **Challenge**               | **Mitigation Strategy**                                                                 |
        |------------------------------|----------------------------------------------------------------------------------------|
        | ERP Data Silos                | Implement **Azure Data Factory** for cross-system ETL.                                   |
        | Skill Gaps in Analytics       | Launch **Udemy for Business** training for audit teams.                                  |
        | False Positives in Anomalies  | Fine-tune models with **historical audit data**.                                         |
        | Resistance to Automation      | Pilot automation in **Plant 3** and showcase ROI.                                       |
        | OT Cybersecurity Risks        | Partner with **Deloitte Cyber** for specialized OT audits.                                |
        """
    )

    st.subheader("Risk Appetite & Technology Adoption")
    st.markdown(
        """
        - **Risk Appetite:** Low for **Financial/Compliance**, Medium for **Operational**, High for **Cybersecurity**.
        - **Tech Stack:**
          - **Analytics:** Python, Power BI, SQL
          - **Automation:** Azure Logic Apps, Power Automate
          - **ETL:** Azure Data Factory, Informatica
          - **ERP:** SAP S/4HANA (primary), Oracle Fusion, EPICOR
        """
    )

# --- Risk & Control Dashboard Tab (Enhanced) ---
with tab2:
    st.header("Risk & Control Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risk Exposure Heatmap")
        risk_data = audit_findings.groupby(["PLANT", "RISK_CATEGORY", "SEVERITY"]).size().reset_index(name="COUNT")
        risk_pivot = risk_data.pivot_table(index=["PLANT", "RISK_CATEGORY"], columns="SEVERITY", values="COUNT", fill_value=0)
        fig = px.imshow(
            risk_pivot,
            labels=dict(x="Severity", y="Plant & Risk Category", color="Count"),
            title="Risk Exposure by Plant & Category",
            color_continuous_scale="RdYlGn_r",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Control Failure Rate & Cost")
        control_data = control_testing[control_testing["RESULT"] == "Fail"]
        failure_rate = control_data.groupby("PLANT").size() / control_testing.groupby("PLANT").size() * 100
        cost_data = control_testing.groupby("PLANT")["COST_PER_TEST_USD"].mean()
        df = pd.DataFrame({"Failure Rate (%)": failure_rate, "Avg Cost per Test (USD)": cost_data}).reset_index()
        fig = px.bar(df, x="PLANT", y=["Failure Rate (%)", "Avg Cost per Test (USD)"], barmode="group", title="Control Performance by Plant")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Audit Cycle Time vs. Severity")
    cycle_time_data = audit_findings.groupby(["SEVERITY", "PLANT"])["AUDIT_CYCLE_TIME_DAYS"].mean().reset_index()
    fig = px.scatter(
        cycle_time_data,
        x="PLANT",
        y="AUDIT_CYCLE_TIME_DAYS",
        color="SEVERITY",
        size="AUDIT_CYCLE_TIME_DAYS",
        title="Audit Cycle Time by Severity & Plant",
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Anomaly & Exception Tab (Enhanced) ---
with tab3:
    st.header("Anomaly & Exception")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Anomaly Types & Resolution Time")
        anomaly_data = anomalies.dropna(subset=["RESOLUTION_TIME_DAYS"])
        fig = px.box(
            anomaly_data,
            x="TYPE",
            y="RESOLUTION_TIME_DAYS",
            title="Anomaly Resolution Time by Type",
            color="TYPE",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Exception Volume & Status")
        exception_data = anomalies["TYPE"].value_counts().reset_index()
        exception_data.columns = ["Type", "Count"]
        fig = px.pie(exception_data, names="Type", values="Count", title="Exception Volume by Type")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Anomaly Detection Trend (Last 12 Months)")
    anomalies["DETECTION_MONTH"] = pd.to_datetime(anomalies["DETECTION_DATE"]).dt.to_period("M").astype(str)
    trend_data = anomalies.groupby("DETECTION_MONTH")["TYPE"].count().reset_index()
    fig = px.line(trend_data, x="DETECTION_MONTH", y="TYPE", title="Monthly Anomaly Detection Trend")
    st.plotly_chart(fig, use_container_width=True)

# --- SOX Compliance Tab (Enhanced) ---
with tab4:
    st.header("SOX Compliance")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("SOX Control Pass Rate by Plant")
        sox_pass_rate = sox_controls[sox_controls["RESULT"] == "Pass"].groupby("PLANT").size() / sox_controls.groupby("PLANT").size() * 100
        fig = px.bar(
            sox_pass_rate.reset_index(),
            x="PLANT",
            y=0,
            title="SOX Control Pass Rate (%)",
            labels={"0": "Pass Rate (%)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("SOX Gaps & Remediation Cost")
        sox_gaps = sox_controls[sox_controls["RESULT"] == "Fail"]
        gap_data = sox_gaps.groupby("PLANT")["REMEDIATION_COST_USD"].sum().reset_index()
        fig = px.bar(gap_data, x="PLANT", y="REMEDIATION_COST_USD", title="SOX Gap Remediation Cost by Plant")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("SOX Remediation Timeline (Gantt Chart)")
    sox_gantt = sox_controls[sox_controls["RESULT"] == "Fail"].copy()
    sox_gantt["START_DATE"] = pd.to_datetime(sox_gantt["TEST_DATE"])
    sox_gantt["END_DATE"] = sox_gantt["START_DATE"] + pd.to_timedelta(sox_gantt["REMEDIATION_COST_USD"] / 1000, unit="D")  # Simulate timeline
    fig = px.timeline(
        sox_gantt,
        x_start="START_DATE",
        x_end="END_DATE",
        y="PLANT",
        color="PLANT",
        title="SOX Remediation Timeline by Plant",
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Data Quality & ETL Tab (Enhanced) ---
with tab5:
    st.header("Data Quality & ETL")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ETL Error Rate by System")
        etl_error_data = etl_metrics[etl_metrics["STATUS"] == "Failed"].groupby("SYSTEM")["ERROR_COUNT"].sum().reset_index()
        fig = px.bar(etl_error_data, x="SYSTEM", y="ERROR_COUNT", title="ETL Errors by System")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("ETL Processing Time")
        etl_time_data = etl_metrics.groupby("SYSTEM")["PROCESSING_TIME_MIN"].mean().reset_index()
        fig = px.bar(etl_time_data, x="SYSTEM", y="PROCESSING_TIME_MIN", title="Avg ETL Processing Time (Minutes)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Quality Trends")
    quality_data = etl_metrics.copy()
    quality_data["SUCCESS_RATE"] = (quality_data["STATUS"] == "Success").astype(int) * 100
    quality_trend = quality_data.groupby(pd.to_datetime(quality_data["JOB_DATE"]).dt.to_period("M").astype(str))["SUCCESS_RATE"].mean().reset_index()
    fig = px.line(quality_trend, x="JOB_DATE", y="SUCCESS_RATE", title="Monthly ETL Success Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

# --- Automation & Scripts Tab (Enhanced) ---
with tab6:
    st.header("Automation & Scripts")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Automation Coverage")
        automation_data = pd.DataFrame({
            "Type": ["Automated", "Manual"],
            "Count": [
                control_testing[control_testing["CONTROL_TYPE"] == "Automated"].shape[0],
                control_testing[control_testing["CONTROL_TYPE"] != "Automated"].shape[0],
            ],
        })
        fig = px.pie(automation_data, names="Type", values="Count", title="Audit Test Automation")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Script Execution Success Rate")
        script_data = pd.DataFrame({
            "Plant": [f"PLANT_{i:03d}" for i in range(1, 5)],
            "Success Rate": [random.randint(85, 99) for _ in range(4)],
        })
        fig = px.bar(script_data, x="Plant", y="Success Rate", title="Script Success Rate by Plant (%)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Automation ROI")
    roi_data = pd.DataFrame({
        "Metric": [
            "Cost Savings (USD/year)",
            "Time Savings (Hours/year)",
            "Error Reduction (%)",
            "Coverage Increase (%)",
        ],
        "Value": [
            round(control_testing["COST_PER_TEST_USD"].mean() * 0.3 * 200, 2),  # 30% savings on 200 tests
            round(audit_findings["AUDIT_CYCLE_TIME_DAYS"].mean() * 8 * 200, 2),  # 200 tests * avg days * 8 hours
            random.randint(20, 40),
            random.randint(15, 30),
        ],
    })
    st.dataframe(roi_data)
