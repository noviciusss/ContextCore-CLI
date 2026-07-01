import asyncio
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# pyrefly: ignore [missing-import]
from agent.graph import build_graph
# pyrefly: ignore [missing-import]
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
# pyrefly: ignore [missing-import]
from rich.console import Console
# pyrefly: ignore [missing-import]
from rich.panel import Panel
# pyrefly: ignore [missing-import]
from rich.text import Text
# pyrefly: ignore [missing-import]
from rich.align import Align
# pyrefly: ignore [missing-import]
from rich.columns import Columns
from agent.mcp_client import get_mcp_client
#thread id identifies a conversation session
# same thread_id = same conversation history

load_dotenv()
console = Console()

def print_banner(thread_id: str):
    """Print ASCII art banner using the art library."""
    try:
        from art import text2art  # pyrefly: ignore [missing-import]
        ascii_art = text2art("ContextCore", font="tarty1")
    except Exception:
        ascii_art = "  ContextCore"

    # Render each line of the ASCII art in a gradient blue→cyan
    banner_text = Text()
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "cyan", "blue"]
    lines = ascii_art.splitlines()
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        banner_text.append(line + "\n", style=f"bold {color}")

    console.print(Align.center(banner_text))
    console.print(
        Align.center(
            Text(
                "Stateful AI Agent  ·  Persistent Memory  ·  MCP Tools",
                style="dim italic",
            )
        )
    )
    console.print(
        Align.center(
            Text(f"thread: {thread_id}  ·  type 'exit' to quit", style="dim")
        )
    )
    console.print()
    console.rule(style="blue dim")
    console.print()

def display_chunk(node: str, output: dict):
    """Pretty-print whatever a node just produced."""

    if node == "intent_router":
        intent = output.get("intent", "")
        color = {
            "task_action": "yellow",
            "memory_recall": "cyan",
            "general_chat": "blue"
        }.get(intent, "white")
        console.print(f"  [dim]◆ Intent[/dim]   [{color}]{intent}[/{color}]")

    elif node == "memory_retriever":
        memories = output.get("retrieved_memory", [])
        profile = output.get("user_profile", {})
        if memories:
            console.print(f"  [dim]◆ Memory[/dim]   [dim]{len(memories)} relevant snippet(s) retrieved[/dim]")
        if profile.get("preferences"):
            prefs = ", ".join(f"{k}={v}" for k, v in profile["preferences"].items())
            console.print(f"  [dim]◆ Profile[/dim]  [dim]{prefs}[/dim]")

    elif node == "agent_executor":
        messages = output.get("messages", [])
        for msg in messages:
            if isinstance(msg, AIMessage):
                # show tool calls if any
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        args = ", ".join(f'{k}="{v}"' for k, v in tc["args"].items())
                        console.print(f"  [dim]◆ Tool[/dim]     [green]{tc['name']}({args})[/green]")
                # show final text response
                elif msg.content:
                    console.print()
                    console.print(
                        Panel(
                            Text(msg.content, style="white"),
                            title="[bold green]Agent[/bold green]",
                            border_style="green",
                            padding=(0, 1)
                        )
                    )

    elif node == "tools":
        messages = output.get("messages", [])
        for msg in messages:
            if isinstance(msg, ToolMessage):
                # truncate long results for display
                content = str(msg.content)
                if len(content) > 120:
                    content = content[:120] + "..."
                console.print(f"  [dim]◆ Result[/dim]  [dim]{content}[/dim]")

    elif node == "memory_writer":
        console.print(f"  [dim]◆ Memory updated[/dim]")

async def main():
    postgres_url = os.getenv("POSTGRES_URL")
    
    with console.status("[bold green]Loading AI models and connecting services...", spinner="dots"):
        from memory.embeddings import get_embedding_model
        get_embedding_model()
        
        mcp_client = get_mcp_client()
        tools = await mcp_client.get_tools()

    async with AsyncPostgresSaver.from_conn_string(postgres_url) as checkpointer:
        await checkpointer.setup()
        graph = await build_graph(tools, checkpointer=checkpointer)

        thread_id = "session-1"
        config = {"configurable": {"thread_id": thread_id}}

        print_banner(thread_id)

        while True:
            try:
                user_input = console.input("[bold blue]You:[/bold blue] ").strip()
            except (KeyboardInterrupt, EOFError):
                break

            if user_input.lower() in ("exit", "quit", "q"):
                console.print("[dim]Goodbye.[/dim]")
                break

            if not user_input:
                continue

            console.print()

            async for chunk in graph.astream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="updates"
            ):
                for node_name, node_output in chunk.items():
                    display_chunk(node_name, node_output)

            console.print()
            console.rule(style="dim")
            console.print()

if __name__ == "__main__":
    import selectors
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))