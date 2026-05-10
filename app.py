import streamlit as st
from huggingface_hub import InferenceClient
import random

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="CodexTutor", layout="wide")

st.sidebar.title("Study Settings")
subject = st.sidebar.selectbox("Subject Focus", ["Math", "Science", "History", "French", "Coding"])
hint_requested = st.sidebar.button("Get a Hint")

if "HF_TOKEN" in st.session_state or "HF_TOKEN" in st.secrets:
    token = st.secrets.get("HF_TOKEN")

    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token=token)
else:
    st.warning("Please add your 'HF_TOKEN' to Streamlit Secrets to enable the AI.")

def get_tutor_response(user_input, is_hint=False):
    if "HF_TOKEN" not in st.secrets:
        return "AI is disconnected. Add your HF_TOKEN to Secrets."

    try:
        client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=st.secrets["HF_TOKEN"])

        if is_hint:
            prompt = f"The student is stuck on this {subject} problem: '{user_input}'. Provide a tiny, helpful hint to nudge them forward, but DO NOT provide the answer."
        else:
            prompt = f"You are CodexTutor, a Socratic {subject} tutor. The student says: '{user_input}'. DO NOT provide the solution. Ask ONE guiding question to help them find it."

        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"

st.title("CodexTutor: AI Socratic Coach")
if "messages" not in st.session_state:
    st.session_state.messages = []

if "messages" in st.session_state:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if user_input := st.chat_input(f"Ask your {subject} question..."):
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = get_tutor_response(user_input)
    with st.chat_message("assistant"):
        st.write(response)
        st.session_state.message.append({"role": "assistant", "content": response})
