import streamlit as st
import sqlite3
import os

# ------------------ Streamlit Title ------------------
st.title(" Patient Records Dashboard")

# ------------------ Ensure Folder Exists ------------------
os.makedirs("healthcare_project/db", exist_ok=True)

# ------------------ Connect to Database ------------------
db_path = "healthcare_project/db/health.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ------------------ Create Table if it doesn't exist ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_metrics (
    patient TEXT PRIMARY KEY,
    bp INTEGER,
    sugar INTEGER
)
""")

# ------------------ Insert Sample Data if Table is Empty ------------------
cursor.execute("SELECT COUNT(*) FROM health_metrics")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Sai", 120, 90),
        ("Sumanth", 120, 90),
        ("Varsha", 80, 90),
        ("Amin", 110, 85),
        ("Sandhya", 115, 88)
    ]
    for record in sample_data:
        cursor.execute("INSERT OR IGNORE INTO health_metrics VALUES (?, ?, ?)", record)
    conn.commit()

# ------------------ Fetch Data ------------------
cursor.execute("SELECT * FROM health_metrics")
rows = cursor.fetchall()

# ------------------ Display in Streamlit ------------------
st.subheader("Patient Records")
st.dataframe(rows)  # Displays as a nice table in the browser

# ------------------ Close Database Connection ------------------
conn.close()