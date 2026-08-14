from agents.tools import hb_classifier
from src.agents import AgentState
import asyncio


async def test_heartbeat_classifier():
    state = await hb_classifier(AgentState(messages=[]))
    print(state)


if __name__ == '__main__':
    asyncio.run(test_heartbeat_classifier())
