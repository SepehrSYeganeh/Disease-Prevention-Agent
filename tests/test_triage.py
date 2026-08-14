from tools import hb_seq_triage, hb_forecaster
from agents.config import AgentState
import asyncio


async def test_triage():
    state = await hb_forecaster(AgentState(messages=[]))
    state = await hb_seq_triage(state)
    print(state)


if __name__ == '__main__':
    asyncio.run(test_triage())
