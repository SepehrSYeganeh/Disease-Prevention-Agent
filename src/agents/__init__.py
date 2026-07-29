from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def graph_builder() -> StateGraph:
    graph = StateGraph(AgentState)

    return graph.compile()


llm = ChatOllama(
    model='ibm/granite4.1:8b',
    streaming=True,
    temperature=0.6
)

agent = graph_builder()
