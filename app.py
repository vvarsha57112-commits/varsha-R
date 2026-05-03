import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import datetime
import speech_recognition as sr
from PIL import Image

from sklearn.ensemble import RandomForestRegressor

# ================= DATABASE =================
DB_NAME = "health.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS health_data (
        name TEXT,
        bp INTEGER,
        sugar INTEGER,
        heart_rate INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= AUTH =================
def register_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

# ================= ML MODEL =================
def train_model():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM health_data", conn)

    if len(df) < 5:
        return None

    X = df[["bp", "sugar"]]
    y = df["heart_rate"]

    model = RandomForestRegressor()
    model.fit(X, y)
    return model

# ================= SMS (OPTIONAL) =================
def send_sms_alert(message):
    # Twilio setup (optional)
    """
    from twilio.rest import Client

    client = Client("ACCOUNT_SID", "AUTH_TOKEN")
    client.messages.create(
        body=message,
        from_="+1234567890",
        to="+91XXXXXXXXXX"
    )
    """
    print("ALERT:", message)

# ================= VOICE INPUT =================
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Could not understand audio"

# ================= IMAGE ANALYSIS =================
def analyze_image(image):
    img = Image.open(image)
    img = img.resize((200, 200))
    return f"Image uploaded successfully. Size: {img.size}"

# ================= UI =================
st.set_page_config(page_title="Health AI Platform", layout="wide")

menu = ["Login", "Register", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(username, password):
            st.success("Account created!")
        else:
            st.error("User already exists")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state["user"] = username
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard":

    if "user" not in st.session_state:
        st.warning("Please login first")
        st.stop()

    st.title("🏥 Health Dashboard")

    user = st.session_state["user"]

    # INPUT
    st.subheader("Enter Health Data")

    bp = st.number_input("Blood Pressure")
    sugar = st.number_input("Sugar")
    heart_rate = st.number_input("Heart Rate")

    if st.button("Save"):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO health_data VALUES (?, ?, ?, ?, ?)",
            (user, bp, sugar, heart_rate, str(datetime.date.today()))
        )
        conn.commit()
        st.success("Saved!")

        if bp > 140 or sugar > 180:
            send_sms_alert("Health Alert!")

    # VIEW DATA
    st.subheader("Your Data")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM health_data WHERE name=?", conn, params=(user,))
    st.dataframe(df)

    # ML PREDICTION
    st.subheader("AI Prediction")

    model = train_model()

    if model:
        pred = model.predict([[bp, sugar]])
        st.success(f"Predicted Heart Rate: {pred[0]:.2f}")
    else:
        st.info("Not enough data")

    # VOICE
    st.subheader("Voice Input")

    if st.button("Start Voice"):
        text = voice_to_text()
        st.write(text)

    # IMAGE
    st.subheader("Upload Medical Image")

    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if file:
        st.image(file)
        st.success(analyze_image(file))     