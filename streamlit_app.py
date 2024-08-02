import streamlit as st

from css_style import get_css_style

# Import PaxMexChatIncidentInfoAgent and PaxMexChatIncidentInfoAgentInput
from agents.pax_mex_chat_incident_info_agent import PaxMexChatIncidentInfoAgent, PaxMexChatIncidentInfoAgentInput

# Get avatar
BOT_AVATAR = "./assets/avatar/grabmerchant.png"

# Import style
style = get_css_style()


# Inject the CSS style
st.markdown(style, unsafe_allow_html=True)

st.title('🦜🔗 PAX-MEX Chat App')

# Add a custom text box outside of st.markdown
st.markdown('<div class="custom-text-box">Heads up! Our AI is still learning, so there might be a hiccup or two. Your keen eye for detail is important to us – please double-check any changes.</div>', unsafe_allow_html=True)

# Initialize the agent
agent = PaxMexChatIncidentInfoAgent()

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
            # Create input object for the agent
            input_data = PaxMexChatIncidentInfoAgentInput(input=prompt, chat_history=st.session_state.messages)
            
            # Get response from the agent
            response = agent.invoke(input_data.dict(), output_key="output")
            
            response_content = response["output"]
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
