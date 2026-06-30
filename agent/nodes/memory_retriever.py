from agent.state import AgentState
from memory.qdrant_store import search_memory
#pyrefly:ignore
from langchain_core.messages import HumanMessage 
from memory.mongo_store import get_profile  
def memory_retriever(state:AgentState)->dict:
    messages = state["messages"]

    last_human = next(
        (m.content for m in reversed(messages) if isinstance(m,HumanMessage)),
        None
    )
    retrived = []
    if last_human:
        retrived = search_memory(last_human,top_k=3)

    # fetch profile from mongodb every turn
    profile = get_profile()

    return {
        "retrieved_memory":retrived,
        "user_profile": profile
    }

    