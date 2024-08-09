import functools
import operator
from typing import Annotated, Any, List, Union, Sequence

from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage, BaseMessage
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate
from langserve.pydantic_v1 import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph

from agents.pax_mex_chat_incident_child_agent import paxMexChatIncidentSummaryAgent,paxMexChatIncidentApologyAgent,paxMexChatIncidentResolutionAgent, paxMexChatLLM
from utils.langgraph import agent_node, draw_mermaid_graph

class PaxMexChatSupervisorAgentInput(BaseModel):
    messages: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        title="messages",
        example=[
            {"type": "human", "content": "Sum of 1+1?"},
        ],
    )


class PaxMexChatSupervisorAgentOutput(BaseModel):
    output: Any

# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str




members = ["Summarize", "Apology"]
def createSupervisorAgent() :
    system_prompt = (
        """
        You are a supervisor tasked with managing a conversation between the
        following workers:  {members}. Given the following user request,
        respond with the worker to act next. Each worker will perform a
        task.
        """
    )
    # Our team supervisor is an LLM node. It just picks the next agent to process
    # and decides when the work is completed
    options = members
    # Using openai function calling can make output parsing easier for us
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                }
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                "Select one of: {options}"
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))

    return (
        prompt
        | paxMexChatLLM.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )


def createPaxMexChatSupervisorAgent() -> CompiledGraph:
    """Creates a simple [ReAct](https://arxiv.org/pdf/2210.03629) agent using LangGraph.
    """

    summaryNode = functools.partial(agent_node, agent=paxMexChatIncidentSummaryAgent, name="Summarize")
    resolutionNode = functools.partial(agent_node, agent=paxMexChatIncidentResolutionAgent, name="Resolution")
    apologyNode = functools.partial(agent_node, agent=paxMexChatIncidentApologyAgent, name="Apology")

    workflow = StateGraph(AgentState)
    workflow.add_node("Summarize", summaryNode)
    workflow.add_node("Resolution", resolutionNode)
    workflow.add_node("Apology", apologyNode)
    workflow.add_node("supervisor", createSupervisorAgent())

    workflow.add_edge("Summarize", "Resolution")

    # The supervisor populates the "next" field in the graph state
    # which routes to a node or finishes
    conditional_map = {k: k for k in members}
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    # Finally, add entrypoint
    workflow.set_entry_point("supervisor")
    workflow.set_finish_point("Resolution")
    workflow.set_finish_point("Apology")

    compiled_graph = workflow.compile()

    # if app_config.is_dev():
    # Draw the graph for visualization
    # This will create a .png file in the same directory as the agent file
    # See ./app/agents/simple_react_agent.png
    draw_mermaid_graph(compiled_graph, __file__)

    return compiled_graph