from agent.state import AgentState
from agent.llm import getllm

llm = getllm()

def responder(state: AgentState)->dict:
    #state.message contains full conversation history
    response = llm.invoke(state["messages"])
    return {"messages": [response]}