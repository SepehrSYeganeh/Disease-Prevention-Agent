from langgraph.graph import StateGraph, START, END
from .config import AgentState, llm
from .router import router
from .response_generator import stream_llm_response


def graph_builder() -> StateGraph:
    graph = StateGraph(AgentState)

    # nodes
    graph.add_node('router', router)
    graph.add_node('response_generator', stream_llm_response)

    # edges
    graph.add_edge(START, 'router')
    graph.add_edge('router', 'response_generator')
    graph.add_edge('response_generator', END)

    return graph.compile()


agent = graph_builder()
