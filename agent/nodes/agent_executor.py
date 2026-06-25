from agent.state import AgentState
from agent.llm import getllm 
# pyrefly: ignore [missing-import]
from langchain_core.messages import SystemMessage 

async def make_agent_executor(tools):
    llm = getllm()
    llm_with_tools = llm.bind_tools(tools)

    async def agent_executor(state: AgentState)->dict:
        messages = state["messages"]
        retrieved = state.get("retrieved_memory",[])

        if retrieved:
            context = "\n".join(retrieved)
            system = SystemMessage(
                content = f"Relevant context from past conversations:\n{context}"
            )
            messages = [system]+ list(messages)
        resposnse  = await llm_with_tools.ainvoke(messages)
        return {"messages": [resposnse]}

    return agent_executor