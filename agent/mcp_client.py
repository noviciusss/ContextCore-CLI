import sys
# pyrefly: ignore [missing-import]
from langchain_mcp_adapters.client import MultiServerMCPClient

def get_mcp_client():
    return MultiServerMCPClient(
        {
            "contextcore":{
                "command": sys.executable,  # use the same venv Python as the main process
                "args":["mcp_server/server.py"],
                "transport":"stdio",
            }
        }
    )