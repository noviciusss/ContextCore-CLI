from agent.state import AgentState
import json 
from memory.mongo_store import update_profile
from memory.qdrant_store import write_memory
from agent.llm import getllm

#pyrefly:ignore 
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
def memory_writer(state:AgentState)->dict:
    messages = state["messages"]
    llm = getllm()

   
    # find the last human message and last AI message this turn
    human_msg = next(
        (m.content for m in reversed(messages) if isinstance(m,HumanMessage)),
        None
    )

    ai_msg = next(
        (m.content for m in reversed(messages) if isinstance(m,AIMessage) and m.content),
        None
    )

    if not  (human_msg and ai_msg):
        return {}

    snippet = f"User said: {human_msg}\nAgent responded: {ai_msg}"
    write_memory(snippet,metadata={"type":"conversation"})

    extraction_prompt = f""" 
    You are analyzing a conversation to extract user prefernces or personal facts. 
    
    User message: "{human_msg}"
    Agent response: "{ai_msg}"

    If the user revealed a preference or fact about themselves (e.g. formatting preferences, 
    communication style, personal details,work habits), extract it as a JSON object with
    short snake_case keys and concise string values.

    If nothing worth storing was revealed return a empty JSON object.

    Return ONLY valid JSON, no explanation. Examples:
    {{"note_format":"bullet points"}}
    {{"name":"Samarth","timezone":"IST"}}
    {{}}
    
    """
    try:
        response = llm.invoke([SystemMessage(content=extraction_prompt)])
        text = response.content.strip()
        #strip markdown code fences if LLM adds them - just a defensive 
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        preferences = json.loads(text)
        if preferences:
            update_profile(preferences)
    except (json.JSONDecodeError,Exception):
        pass # extracting failing silently is fine  - never crash the main turn 

    return {}