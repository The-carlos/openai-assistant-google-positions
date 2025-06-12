# src/app.py

import streamlit as st
from PIL import Image
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils import run_executor

# Load environment variables
load_dotenv()

# Set OpenAI API key and Assistant ID
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)

# Load your logo image (update path if needed)
image = Image.open('src/images/google_logo.png')
image = image.resize((image.width // 4, image.height // 4))
st.image(image)

# App title
st.title("Google Job Assistant – Powered by Carlos Sánchez🤓")

# Initialize thread and chat history in session state
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Typing effect
def typewriter(text: str, speed: int = 50):
    tokens = text.split()
    container = st.empty()
    for i in range(len(tokens) + 1):
        container.markdown(" ".join(tokens[:i]))
        time.sleep(1 / speed)

# User input
if prompt := st.chat_input("Ask me about any Google job position..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        st.spinner("Databot is writing...")

        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        # Create assistant run
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID
        )

        with st.spinner("Processing..."):
            st.toast("Successful conection to Google Cloud Platform, Now the openAI chatbot is working!", icon="🎉")
            run_executor(run)
            response = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            ).data[0].content[0].text.value

        # Display response
        typewriter(response)

    # Save assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": response})
