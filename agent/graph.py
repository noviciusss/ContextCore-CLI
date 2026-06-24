# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START,END
#pyrefly: ignore
from langgraph.prebuilt import ToolNode, tools_condition
from agent.state import AgentState
from agent.nodes.agent_executor import make_agent_executor

async def build_graph(tools,checkpointer=None):
    # creating a graph that uses agentstate as its state schema
    graph = StateGraph(AgentState)

    agent_executor  = await make_agent_executor(tools)
    graph.add_node("agent_executor",agent_executor)
    graph.add_node("tools",ToolNode(tools)) # prebuild langgraph node look at lasr message see it contains a tool call then it calls and put result into state as ToolMessage

    # define the flow: Start->responder->End
    graph.add_edge(START,"agent_executor")
    graph.add_conditional_edges("agent_executor",tools_condition) #tools_cond also prebuilt after agent_executor runs check if there is a tool call if yes route to tools if no route to end
    # if tool call takes place then it goes to tools and then to agent executor 
    graph.add_edge("tools","agent_executor") 

    # compile - pass checkpointer (may be None if not provided)
    return graph.compile(checkpointer=checkpointer)