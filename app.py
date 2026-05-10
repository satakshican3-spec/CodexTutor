import streamlit as st
from huggingface_hub import InferenceClient
import random

st.set_page_config(page_title="CodexTutor", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("Study Settings")
subject = st.sidebar.selectbox("Subject Focus", ["Math", "Science", "History", "French", "Coding"])
hint_requested = st.sidebar.button("Get a Hint")

st.sidebar.write("---")
if "HF_TOKEN" in st.secrets:
    st.sidebar.success("System: Connected")
else:
    st.sidebar.error("System: Missing Token")

def get_tutor_response(user_input, is_hint=False):
    if "HF_TOKEN" not in st.secrets:
        return "Please add your HF_TOKEN to Streamlit Secrets."

    API_URL = "https://huggingface.co"

    if is_hint:
        prompt = f"Student is stuck on {subject}: '{user_input}'. Give a tiny hint, DO NOT give the answer."
    else:
        prompt = f"You are CodexTutor, a Socratic {subject} tutor. Student: '{user_input}'. DO NOT give the solution. Ask ONE guiding question."

    try:
        client = InferenceClient(token=st.secrets["HF_TOKEN"])

        response = client.post(
            json={"inputs": prompt, "parameters": {"max_new_tokens": 150}},
            model=API_URL
        )

        import json
        result = json.loads(response.decode())
        return result[0]['generated_text'].replace(prompt, "").strip()

    except Exception as e:
        return f"Connection Error: {e}. Try checking your token permissions."

st.title("CodexTutor: AI Socratic Coach")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input(f"Ask your {subject} question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Consulting the Codex..."):
            response = get_tutor_response(user_input)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if hint_requested and st.session_state.messages:
    last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), None)
    if last_user_msg:
        with st.chat_message("assistant"):
            hint_text = get_tutor_response(last_user_msg, is_hint=True)
            st.info(f"HINT: {hint_text}")
            st.session_state.messages.append({"role": "assistant", "content": f"HINT: {hint_text}"})
