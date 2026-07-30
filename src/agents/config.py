from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from tools.health_profile import HealthProfile
from tools.biometric_log import BiometricLog


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_profile: HealthProfile | None
    user_biometrics: BiometricLog | None


llm = ChatOllama(
    model='ibm/granite4.1:8b',
    streaming=True,
    temperature=0.6
)
