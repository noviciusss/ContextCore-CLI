# pyrefly: ignore [missing-import]
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP
from db.connection import get_connection
from mcp_server.tools.tasks import register_task_tools
from mcp_server.tools.notes import register_note_tools
mcp = FastMCP("ContextCore")

register_note_tools(mcp)
register_task_tools(mcp)

if __name__ == "__main__":
    from db.connection import init_db
    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Warning: Could not auto-initialize database (is PostgreSQL running?): {e}")
    mcp.run()

    