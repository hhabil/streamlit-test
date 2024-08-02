from typing import Any, List, Union

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from models.azure_openai_model import get_azure_openai_model
from tools.incident_loader_tool import incident_info_loader_tool

class HumanMessage(BaseModel):
    role: str
    content: str

class AIMessage(BaseModel):
    role: str
    content: str

class FunctionMessage(BaseModel):
    role: str
    content: str


class PaxMexChatIncidentInfoAgentInput(BaseModel):
    # This is the input message send to LLM
    input: str = Field(..., title="User input", example="")
    # This is the chat history between the user and the agent.
    # If you don't need a short term memory,
    # You may remove this field and all `chat_history` references in the agent.
    chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        title="Chat history",
        example=[
            {"role": "human", "content": "give me the incidentinfo, incidentID 1123213"},
            {"role": "ai", "content": "orderID:XXX"},
        ],
    )


class PaxMexChatIncidentInfoAgentOutput(BaseModel):
    output: Any


class PaxMexChatIncidentInfoAgent(AgentExecutor):
    def __init__(self) -> None:
        system_prompt = (""" You are an assistant that analyses customer refund request data, then provides a next best resolution. When you are given customer id to look at, use incident_info_loader_tool to get the incidentInfo, then you examine using the following rules:
                    Refund + Voucher: Provide refund if the order had a missing item and the value was high.
                    Immediate Refund: Provide immediate refund if the order had a missing item, and the value was average, and the customer complaint sentiment (extracted_text) is negative.
                    Self-Serve Refund: Provide refund if the item was missing and the value was average, and the customer complaint sentiment (extracted_text) is neutral.
                    Immediate Voucher: Provide an immediate voucher if the item is missing, the value is low, and the customer sentiment is negative (extracted_text).
                    If you find a special item in itemName or under the extracted_text column such as a cake or celebratory item for a party, then flag that as SPECIAL ITEM.
                    If you find an expensive item like waygu steak under the extracted_text column or itemName column, flat this as 'EXPENSIVE ITEM'"""
                        )

        prompt = ChatPromptTemplate.from_messages(
            messages=[
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        tools = [incident_info_loader_tool]
        llm_with_tools = get_azure_openai_model(tools=tools, model_name="gpt-35-turbo", temperature=0.2)

        # The following pipe operators are essentially LangChain Expression Language (LCEL)
        # that used for defines the agent's behavior.
        # Refer https://python.langchain.com/v0.1/docs/expression_language/
        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                    "chat_history": lambda x: x["chat_history"],
                }
                | prompt
                | llm_with_tools
                | OpenAIToolsAgentOutputParser()
        )

        super().__init__(
            agent=agent,
            tools=tools,
            max_execution_time=2 * 60,  # 2 minutes. To prevent infinite loops
            max_iterations=15,  # To prevent infinite loops, adjust as needed
        )
