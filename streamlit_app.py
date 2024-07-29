import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv('secret.env')

st.title('🦜🔗 PAX-MEX Chat App')

# Create function to get response from API
def get_response(input_text):
    headers = {
        'x-tenant-id': os.getenv('X_TENANT_ID'),
        'x-secret-key': os.getenv('X_SECRET_KEY'),
        'x-api-username': os.getenv('X_USERNAME')
    }
    body = {
        "request_id": "unique_request_id",
        "timestamp": 1691719379113,
        "user_prompt": input_text,
        "input_variables": {
        "name": "spellvault"
        }
    }
    try:
        response = requests.post("https://spellvault-gt.stg.mngd.int.engtools.net/ext/completion/ShlK3iTaYO", headers=headers, json=body, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Waiting for response...'):
            response = get_response(prompt)
            response_content = response["chat_history"][1]["content"]
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
