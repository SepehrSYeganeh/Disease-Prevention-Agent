import chainlit as cl
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from . import AgentState, llm


class RequestType(BaseModel):
    request_type: Literal['classification', 'forecasting', 'other'] = Field(
        ...,
        description="Classify if the request requires heartbeat classification, forecasting, or neither."
    )


_req_classifier = llm.with_structured_output(RequestType)

_SYSTEM_PROMPT = SystemMessage(
    content=(
        """
        Classify the user message into one of:
            - 'classification': asks whether a heartbeat is normal or abnormal
            - 'forecasting': asks to predict future heartbeat types or rhythm
            - 'other': anything else
        """
    )
)


async def router(state: AgentState) -> AgentState:
    msg = cl.Message(content="router...")
    await msg.send()

    last_message = state['messages'][-1]
    result: RequestType = await _req_classifier.ainvoke([
        _SYSTEM_PROMPT,
        HumanMessage(content=last_message.content),
    ])
    route = result.request_type

    msg.content = f"next: {route}"
    await msg.update()

    destination_map = {
        'classification': 'classifier',
        'forecasting': 'forecaster',
    }
    return {'next': destination_map.get(route, 'response_generator')}
