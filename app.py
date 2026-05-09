import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="CodexTutor", layout="wide")

quotes = [
    "The mind is not a vessel to be filled, but a fire to be kindled.",
    "Education is the kindling of a flame, not the filling of a vessel.",
    "Knowledge is power. Information is liberating.",
    "A good teacher tells you where to look, but not what to see."
]
st.title("CodexTutor: AI Socratic Coach")
st.write(f"*\"{random.choice(quotes)}\"*")
st.write("---")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Please add your Google API Key to the Streamlit Secrets.")
  
st.sidebar.title("Study Settings")
subject = st.sidebar.selectbox("Subject Focus", ["Math", "Science", "History", "ELA", "French", "Coding"])

st.sidebar.write("Stuck on a step?")
hint_required = st.sidebar.button("Get a Hint")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input(f"Ask your {subject} question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("User"):
        st.write(prompt)

    tutor_prompt = f"You are CodexTutor, a Socratic {subject} tutor. A student asks: {prompt}. " \
                   f"Do Not give the answer. Instead, ask one guiding question to help them find it themselves."

    response = model.generate_content(tutor_prompt)

    with st.chat_message("assistant"):
        st.write(response.text)
        st.session_state.messages.append{"role": "assistant", "content": response.text}
