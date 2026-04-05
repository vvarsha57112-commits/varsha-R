import streamlit as st
import os

st.title("🏗️ AI Project Structure Setup")

# Folders to create
folders = [
    "healthcare_project/app",
    "healthcare_project/db",
    "healthcare_project/data",
    "healthcare_project/utils"
]

# Create folders only once
if "initialized" not in st.session_state:
    for f in folders:
        os.makedirs(f, exist_ok=True)
    st.success("Project structure created successfully ✅")
    st.session_state.initialized = True
else:
    st.info("Project structure already exists")

st.write("Your app is running successfully 🚀")