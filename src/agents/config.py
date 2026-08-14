from typing import TypedDict, Annotated, Literal, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from medicaldb.health_profile import HealthProfileSchema


llm = ChatOllama(
    model='ibm/granite4.1:8b',
    streaming=True,
    temperature=0.6
)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    health_profile_schema: HealthProfileSchema | None
    request: Literal['classification', 'forecasting', 'other']
    hb_class: str | None
    hb_sequence: str | None
    triage_report: dict[str, Any] | None
