import streamlit as st
from get_response_spellvault import get_response_content_spellvault
from get_response_azure import get_response_content_azure

st.title('🦜🔗 PAX-MEX Chat App')

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
            # response_content = get_response_content_spellvault(prompt)
            response_content = get_response_content_azure(prompt)
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
