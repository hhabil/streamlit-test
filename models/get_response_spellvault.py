import streamlit as st
import requests

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

def get_response_content_spellvault(input_text):
    response = get_response(input_text)
    response_content = response["chat_history"][1]["content"]
    return response_content