from agent.state import AgentState
from agent.llm import getllm 
# pyrefly: ignore [missing-import]
from langchain_core.messages import SystemMessage 
import json 

async def make_agent_executor(tools):
    llm = getllm()
    llm_with_tools = llm.bind_tools(tools)

    async def agent_executor(state: AgentState)->dict:
        messages = state["messages"]
        retrieved = state.get("retrieved_memory",[])
        profile = state.get("user_profile",{})

        context_parts = []
        
        if retrieved:
            context_parts.append(
                "Relevant past context:\n"+"\n".join(retrieved)
            )
         # inject structured profile — NEW
        if profile.get("preferences"):
            prefs = json.dumps(profile["preferences"], indent=2)
            context_parts.append(f"User preferences:\n{prefs}")

        if context_parts:
            system = SystemMessage(content="\n\n".join(context_parts))
            messages = [system] + list(messages)

        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    return agent_executor