import streamlit as st
import datetime

def medication_alert(medicine, schedule_time):
    now = datetime.datetime.now().strftime("%H:%M")
    
    if now >= schedule_time:
        return f"Take {medicine} now!"
    else:
        return f"Next dose at {schedule_time}"

st.title("💊 Medication Reminder")

# User inputs
medicine = st.text_input("Enter medicine name:")
time = st.text_input("Enter time (HH:MM):")

# Button to check
if st.button("Check Reminder"):
    if medicine and time:
        result = medication_alert(medicine, time)
        st.write(result)
    else:
        st.write("Please enter all details")