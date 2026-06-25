# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START,END
#pyrefly: ignore
from langgraph.prebuilt import ToolNode, tools_condition
from agent.state import AgentState
from agent.nodes.agent_executor import make_agent_executor
from agent.nodes.memory_retriever import memory_retriever
from agent.nodes.memory_writer import memory_writer

async def build_graph(tools,checkpointer=None):
    # creating a graph that uses agentstate as its state schema
    graph = StateGraph(AgentState)

    agent_executor  = await make_agent_executor(tools)

    graph.add_node("memory_retriever",memory_retriever)
    graph.add_node("agent_executor",agent_executor)
    graph.add_node("tools",ToolNode(tools)) # prebuild langgraph node look at lasr message see it contains a tool call then it calls and put result into state as ToolMessage
    graph.add_node("memory_writer",memory_writer)

    # define the flow: retrive->responder->End
    graph.add_edge(START,"memory_retriever")
    graph.add_edge("memory_retriever","agent_executor")
    graph.add_conditional_edges(
        "agent_executor",
        tools_condition,
        {
            "tools":"tools",
            END:"memory_writer"    #<- intercept END, Write memory first
        }
    )
    graph.add_edge("tools","agent_executor") 
    graph.add_edge("memory_writer",END)

    # compile - pass checkpointer (may be None if not provided)
    return graph.compile(checkpointer=checkpointer)