import streamlit as st
import json
from openai import AzureOpenAI

endpoint = st.secrets["AZURE_CHAT_ENDPOINT"]
deployment = st.secrets["DEPLOYMENT_NAME"]
token_provider = st.secrets["AZURE_API_KEY"]
      
client = AzureOpenAI(
    api_key= token_provider,
    api_version="2024-02-15-preview",
    azure_endpoint = endpoint
)

def get_response_azure (input_text):
    response = client.chat.completions.create(
        model=deployment,
        messages= [
        {
          "role": "user",
          "content": input_text
        }],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return response.to_json()
      
def get_response_content_azure(input_text):
    response = get_response_azure(input_text)
    response_dict = json.loads(response)
    response_content = response_dict["choices"][0]["message"]["content"]
    return response_content