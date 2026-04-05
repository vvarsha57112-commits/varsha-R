
import streamlit as st

def health_chatbot(user_input):
    user_input = user_input.lower()

    if "fever" in user_input:
        return "Stay hydrated and monitor temperature."
    elif "bp" in user_input:
        return "Normal BP is around 120/80."
    elif "medicine" in user_input:
        return "Take medicines on time."
    else:
        return "Please consult a doctor for detailed advice."

# UI input
user_input = st.text_input("Enter your symptoms:")

# Show response
if user_input:
    response = health_chatbot(user_input)
    st.write(response)