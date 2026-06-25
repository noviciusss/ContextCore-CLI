from agent.state import AgentState
from memory.qdrant_store import write_memory
#pyrefly:ignore 
from langchain_core.messages import HumanMessage, AIMessage
def memory_writer(state:AgentState)->dict:
    messages = state["messages"]
    
    # find the last human message and last AI message this turn
    human_msg = next(
        (m.content for m in reversed(messages) if isinstance(m,HumanMessage)),
        None
    )

    ai_msg = next(
        (m.content for m in reversed(messages) if isinstance(m,AIMessage) and m.content),
        None
    )

    if human_msg and ai_msg:
        snippet = f"User said: {human_msg}\nAgent responded: {ai_msg}"
        write_memory(snippet,metadata={"type":"conversation"})

    return {}