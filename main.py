import streamlit as st
import json
import os
import google.generativeai as genai

# Configure API key
API_KEY = "use your own api key"
genai.configure(api_key=API_KEY)

# Initialize GenerativeModel
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Function to authenticate user
def authenticate_user(username, password):
    # Load existing user data
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as json_file:
            user_data = json.load(json_file)
    else:
        user_data = {}

    # Check if username exists and password matches
    if username in user_data and user_data[username] == password:
        return True
    else:
        return False

# Function to save user data
def save_user_data(username, password):
    # Load existing user data
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as json_file:
            user_data = json.load(json_file)
    else:
        user_data = {}

    # Add new user data
    user_data[username] = password

    # Save user data
    with open("user_data.json", "w") as json_file:
        json.dump(user_data, json_file)

# Page title and navigation
st.set_page_config(page_title="CHATMATE", page_icon="🤖", layout="wide")
pages = {
    "Login": "Login",
    "Register": "Register",
    "Chat": "Chat Interface"
}
current_page = st.sidebar.radio("Navigation", list(pages.keys()))

# External background image URL
background_image_url = "https://wallpapercave.com/wp/wp5104136.jpg"

# Custom CSS for styling and background image
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url('{background_image_url}');
        background-size: cover;
    }}
    .stTextInput>div>div>div>input {{
        background-color: #333333; /* Dark Gray */
        border-radius: 15px;
        color: white; /* Text color */
    }}
    .stButton>button {{
        border-radius: 15px;
        background-color: #4CAF50; /* Green */
        color: white;
    }}
    .stText>div>div {{
        background-color: #000000; /* black */
        border-radius: 15px;
        color: white; /* Text color */
    }}
    .stTitle {{
        color: #4CAF50; /* Black color */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title and sidebar
st.title("CHATMATE: THE AI CHATBOT")
st.sidebar.title("Options")

# Login page
if current_page == "Login":
    st.title("CHATMATE: Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.sidebar.success(f"Logged in as: {username}")
        else:
            st.error("Invalid username or password. Please try again.")

# Register page
elif current_page == "Register":
    st.title("CHATMATE: Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    register_button = st.button("Register")

    if register_button:
        if new_username and new_password:
            save_user_data(new_username, new_password)
            st.success("Registration successful! Please login.")
        else:
            st.error("Please enter both username and password.")

# Chat interface
elif current_page == "Chat":
    if st.session_state.get("logged_in"):
        st.title("CHATMATE: Chat Interface")
        user_input = st.text_input("YOU:")
        if st.button("Send"):
            response = chat.send_message(user_input)
            st.text_area("BOT:", value=response.text, height=100)
    else:
        st.error("Please login to access the chat interface.")

# Reset conversation button
if current_page != "Chat" and st.sidebar.button("Reset Conversation"):
    chat = model.start_chat(history=[])  # Reset the chat history

# Display contact information
st.sidebar.header("Contact")
st.sidebar.write("Email: contact@example.com")
st.sidebar.write("Phone: +1 (123) 456-7890")

# Display about us information
st.sidebar.header("About Us")
st.sidebar.write("We are a team dedicated to building cutting-edge AI applications.")