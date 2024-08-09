import operator
import re
import operator
from typing import Annotated, Sequence, TypedDict

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph.graph import CompiledGraph
from langchain_openai import AzureChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: Annotated[str, re.compile(r".*")]
    next_step: Annotated[str, re.compile(r".*")]

def draw_mermaid_graph(compiled_graph: CompiledGraph, agent_file_path: str) -> None:
    """Draws a compiled graph to a mermaid graph file."""
    graph_file_path = agent_file_path.removesuffix(".py") + ".png"
    compiled_graph.get_graph(xray=True).draw_mermaid_png(
        output_file_path=graph_file_path
    )

def create_agent(llm: AzureChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}