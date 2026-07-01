from agent.state import AgentState
from agent.llm import getllm
#pyrefly: ignore
from langchain_core.messages import HumanMessage, SystemMessage


CLASSIFICATION_PROMPT = """ 
Classify the user message into exactly one of these three categories:

- task_action: the user wants to create, list, update, or search tasks or notes
- memory_recall: the user is asking about past conversations, preferences, or something they told you before
- general_chat: anything else — questions, discussion, requests for help

Rules:
- Return ONLY the category label, nothing else, no punctuation
- When in doubt between task_action and another, pick task_action
- "what tasks do I have" = task_action, not memory_recall

User message: "{message}"
"""

def intent_router(state:AgentState) -> dict:
    llm = getllm()
    last_human = next((m.content for m in reversed(state["messages"]) if isinstance(m,HumanMessage)),"")

    prompt = CLASSIFICATION_PROMPT.format(message=last_human)
    response = llm.invoke([SystemMessage(content=prompt)])
    raw = response.content.strip().lower()
    
    #bacause llm talks too much
    if "task_action" in raw:
        intent = "task_action"
    elif "memory" in raw:
        intent = "memory_recall"
    else:
        intent = "general_chat"
    return {"intent" : intent}