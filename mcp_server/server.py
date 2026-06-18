# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ContextCore")

@mcp.tool()
def create_task(title:str, due_data:str = "",priority:str = "medium")->dict:
    """ 
    create new task. 
    Args:
        title: short description of the task
        due_date: optional due date (YYYY-MM-DD)
        priority: low, medium, or high
    """
    return {
        "status":"Created",
        "title":title,
        "due_date":due_data,
        "priority":priority
    }

if __name__ == "__main__":
    create_task()
    