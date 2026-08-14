import chainlit as cl
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from .config import AgentState, llm


class RequestType(BaseModel):
    request_type: Literal['classification', 'forecasting', 'other'] = Field(
        ...,
        description="Classify if the request requires heartbeat classification, forecasting, or neither."
    )


_req_classifier = llm.with_structured_output(RequestType)

_SYSTEM_PROMPT = SystemMessage(
    content="""
    You are an expert ECG analysis router for a medical heart health tracking system.
    Your task is to classify the user's input into one of three specific intents.

    Categories: 
    1. 'classification': User asks to analyze, diagnose, or label a current heartbeat/ECG segment.
    2. 'forecasting': The user asks to predict future trends, future heartbeat classifications, or any 
        heart-health-related future outcome.
    3. 'other': General conversation, greetings, or off-topic queries.

    Examples:
    - Input: "Analyze my heartbeat." -> Output: 'classification'
    - Input: "Is my heart rhythm okay?" -> Output: 'forecasting'
    - Input: "Hello, how are you?" -> Output: 'other'
    """
)


async def router(state: AgentState) -> AgentState:
    msg = cl.Message(content="router...")
    await msg.send()

    last_message = state['messages'][-1]
    result: RequestType = await _req_classifier.ainvoke([
        _SYSTEM_PROMPT,
        HumanMessage(content=last_message.content),
    ])

    msg.content = f"request: {result.request_type}"
    await msg.update()
    return {'request': result.request_type}
