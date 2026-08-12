from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from medicaldb.health_profile import HealthProfileSchema


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_profile: HealthProfileSchema | None
    user_biometrics: dict | None


llm = ChatOllama(
    model='ibm/granite4.1:8b',
    streaming=True,
    temperature=0.6
)
