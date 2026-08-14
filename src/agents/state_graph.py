from langgraph.graph import StateGraph, START, END
from tools import (
    hb_classifier,
    hb_forecaster,
    hb_seq_triage
)
from .config import AgentState
from .router import router
from .response_generator import (
    invalid_request_response,
    hb_classifier_response,
    hb_forecaster_response
)


def _graph_builder() -> StateGraph:
    graph = StateGraph(AgentState)

    # nodes
    graph.add_node('router', router)

    graph.add_node('heartbeat_classifier', hb_classifier)
    graph.add_node('heartbeat_forecaster', hb_forecaster)

    graph.add_node('triage', hb_seq_triage)

    graph.add_node('invalid_request_response', invalid_request_response)
    graph.add_node('hb_classifier_response', hb_classifier_response)
    graph.add_node('hb_forecaster_response', hb_forecaster_response)

    # edges
    graph.add_edge(START, 'router')

    graph.add_conditional_edges(
        "router",
        lambda state: state.get('request'),
        {
            'classification': 'heartbeat_classifier',
            'forecasting': 'heartbeat_forecaster',
            'other': 'invalid_request_response'
        }
    )

    graph.add_edge('invalid_request_response', END)

    graph.add_edge('heartbeat_classifier', 'hb_classifier_response')
    graph.add_edge('hb_classifier_response', END)

    graph.add_edge('heartbeat_forecaster', 'triage')
    graph.add_edge('triage', 'hb_forecaster_response')
    graph.add_edge('hb_forecaster_response', END)

    return graph.compile()


agent = _graph_builder()
