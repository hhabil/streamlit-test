from enum import Enum
import streamlit as st
from typing import Optional, Sequence, List

from langchain_community.tools import BaseTool
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

endpoint = st.secrets["AZURE_CHAT_ENDPOINT"]
deployment = st.secrets["DEPLOYMENT_NAME"]
token_provider = st.secrets["AZURE_API_KEY"]
version = st.secrets["OPENAI_API_VERSION"]
# endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
# deployment = st.secrets["DEPLOYMENT_NAME"]
# token_provider = st.secrets["OPENAI_API_KEY"]
# version = st.secrets["OPENAI_API_VERSION"]

class GrabGPTOpenAIModel(str, Enum):
    """
    Refer https://helix.engtools.net/docs/default/component/integrating_llm_apps_with_grabgpt_developer_guide/onboard-getting-started-connect-your-apps-to-llm_test/#what-available-models-can-i-choose-from
    """

    GPT35_Turbo = "gpt-35-turbo"
    GPT35_Turbo_16K = "gpt-35-turbo-16k"
    GPT4 = "gpt-4"
    GPT4_32K = "gpt-4-32k"
    GPT4_TURBO = "gpt-4-turbo"
    GPT4_TURBO_VISION = "gpt-4-turbo-vision"
    GPT4O = "gpt-4o"
    ADA_002 = "text-embedding-ada-002"

    def __str__(self) -> str:
        return str(self.value)


def get_openai_model(
    model_name: Optional[GrabGPTOpenAIModel] = GrabGPTOpenAIModel.GPT4_32K,
    timeout: Optional[int] = 60,
    tools: Optional[Sequence[BaseTool]] = None,
    temperature: Optional[float] = 0.7,
) -> Runnable:
    """return AzureChatOpenAI model with tools."""

    azure_chat_openai = ChatOpenAI(
        base_url=endpoint + "/v1",
        api_key=token_provider,
        model_name=model_name.__str__(),
        timeout=timeout,
        temperature=temperature,
        streaming=True,
    )

    if not tools:
        return azure_chat_openai

    return azure_chat_openai.bind_tools(tools)
