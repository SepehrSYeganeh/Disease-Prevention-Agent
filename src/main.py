from langchain_core.messages import HumanMessage, AIMessage
import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import ThreadDict
from dotenv import load_dotenv
import os
from agents import agent
from agents.config import AgentState

load_dotenv()


@cl.on_chat_start
async def start():
    cl.user_session.set('state', AgentState(messages=[]))
    await cl.Message(content="Hello! How can I help you?").send()


@cl.on_message
async def on_message(message: cl.Message):
    state = cl.user_session.get('state')
    state['messages'].append(HumanMessage(content=message.content))
    final_state = await agent.ainvoke(state)
    cl.user_session.set('state', final_state)


@cl.on_stop
async def on_stop():
    print("The user session has ended")


@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if username == "admin" and password == "admin":
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None


@cl.data_layer
def get_data_layer():
    conninfo = os.getenv("DATABASE_URL")
    if not conninfo:
        print("\nDATABASE_URL not found in environment variables.")
        return None

    try:
        data_layer = SQLAlchemyDataLayer(conninfo=conninfo)
        return data_layer
    except Exception as e:
        print(f"\n\nFailed to initialize SQLAlchemyDataLayer: {e}")
        return None


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    try:
        steps = thread.get("steps", [])
        messages = []
        for step in steps:
            step_type = step.get("type")
            content = (step.get("output") or "").strip()
            if not content:
                continue  # skip empty rows

            if step_type == "user_message":
                messages.append(HumanMessage(content=content))
            elif step_type == "assistant_message":
                messages.append(AIMessage(content=content))
        cl.user_session.set("state", {"messages": messages})

    except Exception as e:

        print(f"\nError resuming chat: {e}")
        cl.user_session.set("state", {"messages": []})
