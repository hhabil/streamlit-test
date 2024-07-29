import streamlit as st
import requests

st.title('🦜🔗 PAX-MEX Chat App')

# Create function to get response from API
def get_response(input_text):
    headers = {
        'x-tenant-id': st.secrets['X_TENANT_ID'],
        'x-secret-key': st.secrets['X_SECRET_KEY'],
        'x-api-username': st.secrets['X_USERNAME']
    }
    body = {
        "request_id": "unique_request_id",
        "timestamp": 1691719379113,
        "user_prompt": input_text,
        "input_variables": {
        "name": "spellvault"
        }
    }
    response = requests.post("https://spellvault-gt.stg.mngd.int.engtools.net/ext/completion/ShlK3iTaYO", headers=headers, json=body)
    return response.json()

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
