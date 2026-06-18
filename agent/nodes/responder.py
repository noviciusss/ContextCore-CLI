from agent.state import AgentState
from agent.llm import getllm

llm = getllm()

def responsder(state: AgentState)->dict:
    #state.message comtains full conversation history
    reponse = llm.invoke(state["messages"])
    return {"messages": [reponse]}