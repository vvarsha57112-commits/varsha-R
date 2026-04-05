


import streamlit as st
import sqlite3

st.title("Healthcare Assistant")

user_input = st.text_input("Ask health question:")

if user_input:
    if "fever" in user_input.lower():
        st.write("Stay hydrated!")
    else:
        st.write("Consult doctor")

st.subheader("Add Health Data")

name = st.text_input("Patient Name")
bp = st.number_input("BP")
sugar = st.number_input("Sugar")
name = st.text_input("patient sumanth")
bp = st.number_input("95/100")
sugar = st.text_input("120")


if st.button("Save"):
    conn = sqlite3.connect("health.db")
    c = conn.cursor()
    c.execute("INSERT INTO health_metrics VALUES (?, ?, ?)", (name, bp, sugar))
    conn.commit()
    st.success("Saved!")