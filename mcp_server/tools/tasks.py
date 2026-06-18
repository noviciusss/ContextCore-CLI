from db.connection import get_connection

def register_task_tools(mcp):

    @mcp.tool()
    def create_task(title: str, due_date: str = "", priority: str = "medium") -> dict:
        """Create a new task with title, optional due date, and priority."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, due_date, priority) VALUES (%s, %s, %s) RETURNING *",
                    (title, due_date or None, priority)
                )
                row = cur.fetchone()
                conn.commit()
            return dict(row)
        finally:
            conn.close()
    @mcp.tool()
    def list_tasks(status: str="")-> list:
        """List tasks, optionaly filtered by status (pending,in-progress,completed)"""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                if status:
                    cur.execute(
                        "SELECT * FROM tasks WHERE status= %s ORDER BY created_at DESC",
                      (status,)
                    )
                else:
                    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
                rows  = cur.fetchall()
                return [dict(row) for row in rows]
        finally:
            conn.close()
    @mcp.tool()
    def upadate_task(task_id:int,status:str="",priority:str="")->dict:
        """Update a task's status and/or priotiry by its Id."""
        con = get_connection()
        try:
            with con.cursor() as cur:
                if status:
                    cur.execute(
                        "UPDATE tasks SET status = %s WHERE id = %s",(status,task_id)
                    )
                if priority:
                    cur.execute(
                        "UPDATE tasks SET priority= %s WHERE id = %s",(priority,task_id)
                    )
                con.commit()
                cur.execute("SELECT * FROM tasks WHERE id =%s",(task_id,))
                row = cur.fetchone()
                return dict(row) if row else {"error": "task not found"}
        finally:
                con.close()