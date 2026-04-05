import streamlit as st
import sqlite3
import os
import pandas as pd

# ---------- CREATE FOLDER ----------
os.makedirs("healthcare_project/db", exist_ok=True)

# ---------- CONNECT DATABASE ----------
db_path = "healthcare_project/db/health.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# ---------- CREATE TABLE ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_metrics (
    patient TEXT PRIMARY KEY,
    bp INTEGER,
    sugar INTEGER
)
""")

# ---------- INSERT DEFAULT DATA ----------
data = [
    ("Sai", 120, 90),
    ("Sumanth", 120, 90),
    ("Varsha", 80, 90),
    ("Amin", 110, 85),
    ("Sandhya", 115, 88)
]

for record in data:
    cursor.execute(
        "INSERT OR IGNORE INTO health_metrics VALUES (?, ?, ?)",
        record
    )

conn.commit()

# ---------- STREAMLIT UI ----------
st.title("🏥 Healthcare App")

# Show data
df = pd.read_sql_query("SELECT * FROM health_metrics", conn)

st.subheader("📊 Patient Records")
st.dataframe(df)

# Add new patient
st.subheader("➕ Add Patient")

name = st.text_input("Patient Name")
bp = st.number_input("Blood Pressure", min_value=0)
sugar = st.number_input("Sugar Level", min_value=0)

if st.button("Add"):
    try:
        cursor.execute(
            "INSERT INTO health_metrics VALUES (?, ?, ?)",
            (name, bp, sugar)
        )
        conn.commit()
        st.success("Added successfully ✅")
    except:
        st.warning("Duplicate entry ⚠️")