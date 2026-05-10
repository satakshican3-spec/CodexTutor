import streamlit as st
from huggingface_hub import InferenceClient
import random

st.set_page_config(page_title="CodexTutor", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("Study Settings")
subject = st.sidebar.selectbox("Subject Focus", ["Math", "Science", "History", "French", "Coding"])
hint_requested = st.sidebar.button("Get a Hint")

if "HF_TOKEN" in st.secrets:
    client = InferenceClient(model="google/gemma-2b-it", token=st.secrets["HF_TOKEN"])
else:
    st.warning("Please add your 'HF_TOKEN' to Streamlit Secret to enable the AI.")

def get_tutor_response(user_input, is_hint=False):
    if "HF_TOKEN" not in st.secrets:
        return "AI is disconnected. Please add your token."

    if is_hint:
        prompt = f"The student stuck on this {subject} problem: '{user_input}'. Provide a tiny, helpful hint, but DO NOT give the answer."
    else:
        prompt = f"You are CodexTutor, a Socratic {subject} tutor. The student says: '{user_input}'. DO NOT provide the solution. Ask ONE guiding question to help them find it."

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        
        try:
            temp_client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=st.secrets["HF_TOKEN"])
            resp = temp_client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=150)
            return resp.choices[0].message.content
        except:
            return f"AI System Error: {e}. Please try again in 10 seconds."

st.title("CodexTutor: AI Socratic Coach")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input(f"Ask your {subject} question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_tutor_response(user_input)
            st.write(response)
            st.session_state.messages.append({"role": "assistance", "content": response})

if hint_requested and st.session_state.messages:
    last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), None)
    if last_user_msg:
        with st.chat_message("assistance"):
            hint_text = get_tutor_response(last_user_msg, is_hint=True)
            st.info(f"HINT: {hint_text}")
            st.session_state.messages.append({"role": "assistant", "content": f"HINT: {hint_text}"})
