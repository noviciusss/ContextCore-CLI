import asyncio
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# pyrefly: ignore [missing-import]
from agent.graph import build_graph
# pyrefly: ignore [missing-import]
from langchain_core.messages import HumanMessage
from agent.mcp_client import get_mcp_client 
#thread id identifies a conversation session
# same thread_id = same conversation history

load_dotenv() 

async def main(): 
    postgres_url = os.getenv("POSTGRES_URL")
    mcp_client = get_mcp_client()
    tools= await mcp_client.get_tools()

    async with AsyncPostgresSaver.from_conn_string(postgres_url) as checkpointer:
        await checkpointer.setup()

        graph = await build_graph(tools,checkpointer=checkpointer)
        config  = {"configurable": {"thread_id": "session-1"}}

        print("ContextCore CLI — type 'exit' to quit")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            # wrap input as HumanMessage 
            result = await graph.ainvoke(
                {
                    "messages": [HumanMessage(content=user_input)]
                }, config = config)
            #last message instance is the assistants reply     
            for msg in result["messages"][-3:]:
                print(f"[{msg.type}] {msg.content}")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())