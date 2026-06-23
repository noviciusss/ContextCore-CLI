from agent.state import AgentState
from agent.llm import getllm 

async def make_agent_executor(tools):
    llm = getllm()
    llm_with_tools = llm.bind_tools(tools)

    async def agent_executor(state: AgentState)->dict:
        resposnse  = await llm_with_tools.ainvoke(state["messages"])
        return {"messages": [resposnse]}

    return agent_executor