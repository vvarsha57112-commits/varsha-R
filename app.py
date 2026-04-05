
import streamlit as st
import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect("health.db",
    check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        name TEXT,
        bp INTEGER,
        sugar INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Insert data
def insert_data(name, bp, sugar):
    conn = sqlite3.connect("health.db")
    c = conn.cursor()
    c.execute("INSERT INTO health_metrics VALUES (?, ?, ?)", (name, bp, sugar))
    conn.commit()
    conn.close()

# Fetch data
def get_data():
    conn = sqlite3.connect("health.db")
    df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
    conn.close()
    return df

# UI
st.title("Healthcare Assistant")

name = st.text_input("Enter Name")
bp = st.number_input("Blood Pressure", 0, 300)
sugar = st.number_input("Sugar Level", 0, 500)

if st.button("Save Data"):
 if name.strip() and bp > 0 and sugar > 0:
    insert_data(name, bp, sugar)
    st.success("Data saved successfully!")

# Show table
st.subheader("Stored Data")
st.dataframe(get_data())

conn = sqlite3.connect("health.db")
df = pd.read_sql_query("SELECT * FROM health_metrics", conn)
conn.close()

st.write("Stored Data")
st.dataframe(df)
