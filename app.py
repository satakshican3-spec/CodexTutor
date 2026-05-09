import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="CodexTutor", layout="wide")

st.title("CodexTutor: AI Socratic Coach")

quotes = [
    "The mind is not a vessel to be filled, but a fire to be kindled.",
    "Knowledge is the result of self-discovery.",
    "A good teacher tells you where to look, but not what to see."
]
st.write(f"*\"{random.choice(quotes)}\"*")
st.write("---")

model = None

if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
else:
    st.warning("Please add your 'GOOGLE_API_KEY' to Streamlit Secrets to enable the AI.")

st.sidebar.write("Stuck on a step?")
hint_requested = st.sidebar.button("Get a Hint")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_tutor_response(user_input, is_hint=False):
    if model is None:
        return "AI is not connected. Please check your API key."

    if is_hint:
        instruction = f"The student is stuck on this {subject} problem: '{user_input}'. Give a tiny, helpful hint to nudge them forward, but DO NOT give the answer."
    else:
        instruction = f"You are CodexTutor, a Socratic {subject} tutor. The student says: '{user_input}'. DO NOT give the solution. Ask One guiding question to help them find it."

    try:
        response = model.generate_content(instruction)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

if prompt := st.chat_input(f"Ask your {subject} question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response_text = get_tutor_response(prompt)

    with st.chat_message("assistant"):
        st.write(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if hint_requested and st.session_state.messages:
    last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), None)
    with st.chat_message("assistant"):
        st.info(f"HINT: {hint_text}")
        st.session_state.messages.append({"role": "assistant", "content": f"HINT: {hint_text}"})

