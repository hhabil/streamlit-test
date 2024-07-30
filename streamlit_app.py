import streamlit as st
from get_response_spellvault import get_response_content_spellvault
from get_response_azure import get_response_content_azure
from css_style import get_css_style

# Get avatar
BOT_AVATAR = "./assets/avatar/grabmerchant.png"

# Import style
style = get_css_style()


# Inject the CSS style
st.markdown(style, unsafe_allow_html=True)

st.title('🦜🔗 PAX-MEX Chat App')

# Add a custom text box outside of st.markdown
st.markdown('<div class="custom-text-box">Heads up! Our AI is still learning, so there might be a hiccup or two. Your keen eye for detail is important to us – please double-check any changes.</div>', unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar=BOT_AVATAR):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner('Waiting for response...'):
            # response_content = get_response_content_spellvault(prompt)
            response_content = get_response_content_azure(prompt)
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
