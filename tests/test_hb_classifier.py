from src.tools import heartbeat_classifier
from src.agents import AgentState
import asyncio


async def test_heartbeat_classifier():
    state = await heartbeat_classifier(AgentState(messages=[]))
    print(state)


if __name__ == '__main__':
    asyncio.run(test_heartbeat_classifier())
