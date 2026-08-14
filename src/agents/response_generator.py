from langchain_core.messages import AIMessage
import chainlit as cl
import asyncio
from .config import AgentState, llm


async def stream_llm_response(state: AgentState) -> AgentState:
    msg = cl.Message(content="")
    await msg.send()

    content = ""
    try:
        async for chunk in llm.astream(state['messages']):
            if chunk.content:
                content += chunk.content
                await msg.stream_token(chunk.content)
    except asyncio.CancelledError:
        print("\nStreaming was interrupted.")
        pass

    await msg.update()
    return {'messages': AIMessage(content=content)}


async def hb_forecaster_response(state: AgentState) -> AgentState:
    content = f"Your forecasted heart beats are {state.get('hb_sequence')}"
    await cl.Message(content=content).send()
    return {'messages': AIMessage(content=content)}


async def hb_classifier_response(state: AgentState) -> AgentState:
    content = f"Your heartbeat class is {state.get('hb_class')}."
    await cl.Message(content=content).send()
    return {'messages': AIMessage(content=content)}


async def invalid_request_response(state: AgentState) -> AgentState:
    content = "Invalid request."
    await cl.Message(content=content).send()
    return {'messages': AIMessage(content=content)}
