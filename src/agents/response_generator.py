from langchain_core.messages import AIMessage
import chainlit as cl
import asyncio


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
