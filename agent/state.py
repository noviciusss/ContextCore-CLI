from typing import TypedDict, Annotated
# pyrefly:ignore 
from langgraph.graph import add_messages


class AgentState(TypedDict):
    messages:Annotated[list,add_messages]
    retrieved_memory: list[str] # <- populated by memory_retriever 