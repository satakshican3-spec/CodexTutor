import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="CodexTutor", layout="wide")

st.sidebar.title("Study Settings")
subject = st.sidebar.selectbox("Subject Focus", ["Math", "Science", "History", "French", "Coding"])

st.sidebar.write("Stuck on a step?")
hint_requested = st.sidebar.button("Get a Hint")

st.sidebar.write("---")
st.sidebar.subheader("System Status")

If "GOOGLE_API_KEY" in st.secrets:
    st.sidebar.success("AI Engine: Connected")
    api_connected = True
else:
    st.sidebar.error("AI Engine: Disconnected")
    api_connected = False

with st.sidebar.expander("Setup Guide: How to connect"):
    st.write("""
    1. Visit [Google AI Studio](https://google.com).
    2. Click 'Get API key' and copy your key.
    3. In your Streamlit Dashboard, go to Settings > Secrets.
    4. Paste your key exactly like this:
       GOOGLE_API_KEY = "your-key-here"
    """)

st.title("CodexTutor: AI Socratic Coach")

quotes = [
    "The mind is not a vessel to be filled, but a fire to be kindled.",
    "Knowledge is the result of self-discovery.",
    "A good teacher tells you where to look, but not what to see."
]
st.write(f"*\"{random.choice(quotes)}\"*")
st.write("---")

model = None

if api_connected:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.sidebar.error(f"API Error: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_tutor_response(user_input, is_hint=False):
    if model is None:
        return "The AI engine is currently disconnected. Please follow the setup guide in the sidebar."

    if is_hint:
        instruction = f"The student is stuck on this {subject} problem: '{user_input}'. Provide a small, helpful hint to nudge them forward, but DO NOT reveal the final answer."
    else:
        instruction = f"You are CodexTutor, a Socratic {subject} tutor. The student says: '{user_input}'. DO NOT Provide the solution. Ask one strategic question to help them find it."

    try:
        response = model.generate_content(instruction)
        return response.text
    except Exception as e:
        return f"System Error: {e}"

if prompt := st.chat_input(f"Enter your {subject} question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response_text = get_tutor_response(prompt)

    with st.chat_message("assistant"):
        st.write(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if hint_requested and st.session_state.messages:
    last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), None)

    if last_user_msg:
        hint_text = get_tutor_response(last_user_msg, is_hint=True)
        with st.chat_message("assistant"):
            st.info(f"HINT: {hint_text}")
            st.session_state.messages.append({"role": "assistance", "content": f"HINT: {hint_text}"})
