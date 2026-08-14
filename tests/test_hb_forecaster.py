from src.tools import heartbeat_forecaster
from src.agents import AgentState
import asyncio


async def test_heartbeat_forecaster():
    state = await heartbeat_forecaster(AgentState(messages=[]))
    print(state)


if __name__ == '__main__':
    asyncio.run(test_heartbeat_forecaster())
