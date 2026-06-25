from agent.state import AgentState
from memory.qdrant_store import search_memory
#pyrefly:ignore
from langchain_core.messages import HumanMessage 

def memory_retriever(state:AgentState)->dict:
    messages = state["messages"]

    last_human = next(
        (m.content for m in reversed(messages) if isinstance(m,HumanMessage)),
        None
    )

    if not last_human:
        return {"retrieved_memory" :[]}

    relevant = search_memory(last_human,top_k=3)
    return {"retrieved_memory": relevant}

    