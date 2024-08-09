import streamlit as st

from css_style import get_css_style

# Import PaxMexChatIncidentInfoAgent and PaxMexChatIncidentInfoAgentInput
# from agents.pax_mex_chat_incident_info_agent import PaxMexChatIncidentInfoAgent, PaxMexChatIncidentInfoAgentInput
from agents.pax_mex_chat_supervisor_agent import createPaxMexChatSupervisorAgent, PaxMexChatSupervisorAgentInput

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
agent = createPaxMexChatSupervisorAgent
# agent = PaxMexChatIncidentInfoAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["type"] == "ai":
        with st.chat_message(message["type"], avatar=BOT_AVATAR):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["type"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("human"):
        st.markdown(prompt)
    st.session_state.messages.append({"type": "human", "content": prompt})

    with st.spinner('Waiting for response...'):
        full_response = ""

        # Create input object for the agent
        input_data = PaxMexChatSupervisorAgentInput(messages=st.session_state.messages)
        
        # Stream the response from the agent
        for chunk in agent().stream(input_data.dict()):
            if "Resolution" in chunk or "Apology" in chunk:
                if "Resolution" in chunk:
                    full_response += chunk["Resolution"]["messages"][0].content
                if "Apology" in chunk:
                    full_response += chunk["Apology"]["messages"][0].content

    with st.chat_message("ai", avatar=BOT_AVATAR):
        st.markdown(full_response)
    st.session_state.messages.append({"type": "ai", "content": full_response})
