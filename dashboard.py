import pandas as pd
import mysql.connector
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Machine Maintenance Dashboard", layout="wide")

st.title("🔧 Machine Maintenance Dashboard")

# --------------------------
# Step 1: Connect to MySQL
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Khushi@1608",
    database="project"
)

# --------------------------
# Step 2: Load Predictions table
# --------------------------
query = "SELECT * FROM Predictions;"
df = pd.read_sql(query, conn)
conn.close()

# --------------------------
# Step 3: Overview Metrics
# --------------------------
st.subheader("Overview")
total_readings = len(df)
alerts = df['alert_flag'].sum()
st.metric("Total Readings", total_readings)
st.metric("Total Alerts", alerts)

# --------------------------
# Step 4: Alert Distribution
# --------------------------
st.subheader("Alert Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(x='alert_flag', data=df, ax=ax1)
ax1.set_xticklabels(["No Alert", "Alert"])
st.pyplot(fig1)

# --------------------------
# Step 5: Probability Histogram
# --------------------------
st.subheader("Failure Probability Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(df['fail_prob'], bins=20, kde=True, ax=ax2)
ax2.set_xlabel("Failure Probability")
st.pyplot(fig2)

# --------------------------
# Step 6: Machine-wise Alerts
# --------------------------
st.subheader("Alerts by Machine")
machine_alerts = df.groupby('machine_id')['alert_flag'].sum().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(x='machine_id', y='alert_flag', data=machine_alerts, ax=ax3)
ax3.set_xlabel("Machine ID")
ax3.set_ylabel("Number of Alerts")
st.pyplot(fig3)
