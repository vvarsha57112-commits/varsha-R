import streamlit as st
import datetime
import time

st.title("💊 Medication Reminder")

medicine = st.text_input("Medicine Name", "Paracetamol")
schedule_time = st.text_input("Scheduled Time (HH:MM)", "09:00")

# Button to check medication
if st.button("Check Medication Time"):
    now = datetime.datetime.now().strftime("%H:%M")
    if now == schedule_time:
        st.success(f"⏰ Take {medicine} now!")
    else:
        st.info(f"Not time yet. Current time: {now}")