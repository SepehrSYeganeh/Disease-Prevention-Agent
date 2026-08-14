import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.types import ThreadDict
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv
import os
import hashlib

from agents import agent
from agents import AgentState
from medicaldb.health_profile import (
    get_user_health_profile,
    upsert_user_health_profile,
    user_health_profile_to_schema
)

load_dotenv()

# ============ DATA LAYER ============

data_layer = SQLAlchemyDataLayer(
    conninfo=os.getenv("DATABASE_URL"),
    show_logger=True
)


@cl.data_layer
def get_data_layer() -> SQLAlchemyDataLayer:
    return data_layer


# ============ AUTH ============

def hash_password(password: str) -> str:
    """Returns a simple SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    """Compares the incoming password hash with the stored hash."""
    return hash_password(password) == stored_hash


@cl.password_auth_callback
async def auth_callback(username: str, password: str) -> cl.User | None:
    identifier = username.strip().lower()
    if not identifier or not password:
        return None

    existing_user = await data_layer.get_user(identifier)

    # log in
    if existing_user:
        stored_hash = existing_user.metadata.get("password_hash") if existing_user.metadata else None
        if stored_hash and verify_password(password, stored_hash):
            return cl.User(
                identifier=existing_user.identifier,
                metadata=existing_user.metadata
            )
        else:
            return None

    # sign up
    else:
        password_hash = hash_password(password)
        new_user = cl.User(
            identifier=identifier,
            metadata={"password_hash": password_hash}
        )

        persisted_user = await data_layer.create_user(new_user)
        if persisted_user:
            return cl.User(
                identifier=persisted_user.identifier,
                metadata=persisted_user.metadata
            )
        return None


# ============ CHAT ============

async def get_hps(identifier: str):
    uhp = await get_user_health_profile(identifier)
    if uhp is None:
        first_name = await cl.AskUserMessage(content="What is your first name?").send()
        last_name = await cl.AskUserMessage(content="What is your last name?").send()
        age = await cl.AskUserMessage(content="What is your age?").send()
        sex = await cl.AskUserMessage(content="What is your sex? [M, F, X]").send()
        height = await cl.AskUserMessage(content="What is your height (cm)?").send()
        weight = await cl.AskUserMessage(content="What is your weight (kg)?").send()

        uhp = await upsert_user_health_profile(
            identifier=identifier,
            first_name=first_name.get('output'),
            last_name=last_name.get('output'),
            age=int(age.get('output')),
            sex=sex.get('output'),
            height=float(height.get('output')),
            weight=float(weight.get('output'))
        )

    return await user_health_profile_to_schema(uhp)


@cl.on_chat_start
async def start():
    user: cl.User = cl.user_session.get("user")
    cl.user_session.set("identifier", user.identifier)

    hps = await get_hps(user.identifier)

    cl.user_session.set(
        'state',
        AgentState(
            messages=[],
            health_profile_schema=hps
        )
    )

    await cl.Message(content=f"Hello {user.identifier}! How can I help you?").send()


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


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    try:
        steps = thread.get('steps', [])
        messages = []
        for step in steps:
            step_type = step.get('type')
            content = (step.get('output') or '').strip()
            if not content:
                continue

            if step_type == 'user_message':
                messages.append(HumanMessage(content=content))
            elif step_type == 'assistant_message':
                messages.append(AIMessage(content=content))

        user: cl.User = cl.user_session.get("user")
        cl.user_session.set("identifier", user.identifier)
        hps = await get_hps(user.identifier)
        cl.user_session.set(
            'state',
            AgentState(
                messages=messages,
                health_profile_schema=hps
            )
        )

    except Exception as e:
        print(f"\nError resuming chat: {e}")
        cl.user_session.set(
            'state',
            AgentState(
                messages=[],
                health_profile_schema=None
            )
        )
