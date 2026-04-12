import streamlit as st
import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect("health.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        name TEXT,
        bp INTEGER,
        sugar INTEGER
    )
    """)

    # ✅ FORCE CREATE TABLE (fix)
    c.execute("DROP TABLE IF EXISTS health")

    c.execute("""
    CREATE TABLE health(
        name TEXT,
        steps INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()


# Insert data
def insert_data(name, bp, sugar):
    conn = sqlite3.connect("health.db")
    c = conn.cursor()

    # ❌ REMOVED input from here

    c.execute("INSERT INTO health_metrics VALUES (?, ?, ?)", (name, bp, sugar))

    # ✅ use steps from UI
    c.execute("INSERT INTO health VALUES (?, ?)", (name, steps))

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

# ✅ FIX: moved here
steps = st.number_input("Enter steps walked")
calories = st.number_input("Calories burned")

if st.button("Save Data"):
    insert_data(name, bp, sugar)
    st.success("Data saved successfully!")


# Show table
st.subheader("Stored Data")
st.dataframe(get_data())


# Show steps table
conn = sqlite3.connect("health.db")

try:
    df = pd.read_sql_query("select * from health", conn)
    st.write("Steps Data")
    st.dataframe(df)
except:
    st.warning("No data yet")

conn.close()
st.subheader("Health Chart")

df = get_data()

if not df.empty:
    st.line_chart(df)
goal = st.number_input("Set Step Goal")

if steps >= goal:
    st.success("Goal completed 🎉")
else:
    st.warning("Try more steps")