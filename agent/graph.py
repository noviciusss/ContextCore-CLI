# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START,END
from agent.state import AgentState
from agent.nodes.responder import responsder

def build_graph(tools,checkpointer=None):
    # creating a graph that uses agentstate as its state schema
    graph = StateGraph(AgentState)

    # add the responder node - just one for now
    graph.add_node("responder",responsder)

    # define the flow: Start->responder->End
    graph.add_edge(START,"responder")
    graph.add_edge("responder",END)

    # compile - pass checkpointer (may be None if not provided)
    return graph.compile(checkpointer=checkpointer)