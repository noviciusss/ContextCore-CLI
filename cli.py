import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from agent.graph import build_graph
from langchain_core.messages import HumanMessage

#thread id identifies a conversation session
# same thread_id = same conversation history

load_dotenv() 

def main(): 
    postgres_url = os.getenv("POSTGRES_URL")

    with PostgresSaver.from_conn_string(postgres_url) as checkpointer:
        checkpointer.setup()

        graph = build_graph(checkpointer=checkpointer)
        config  = {"configurable": {"thread_id": "session-1"}}

        print("ContextCore CLI — type 'exit' to quit")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            # wrap input as HumanMessage 
            result = graph.invoke(
                {
                    "messages": [HumanMessage(content=user_input)]
                }, config = config)
            #last message instance is the assistants reply     
            print("Agent:",result["messages"][-1].content)
if __name__ == "__main__":
    main()