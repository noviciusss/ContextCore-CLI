from db.connection import get_connection

def register_note_tools(mcp):
  
   @mcp.tool()
   def save_note(content: str, tags: str = "") -> dict:
        """Save a note. Tags are optional, comma-separated."""
        tag_list = [t.strip() for t in tags.split(",")] if tags else []
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO notes (content, tags) VALUES (%s, %s) RETURNING *",
                    (content, tag_list)
                )
                row = cur.fetchone()
                conn.commit()
            return dict(row)
        finally:
            conn.close()
   @mcp.tool()
   def search_notes(query:str)->list:
        """Search notes by keyword. (basic text_match - upgarding to sementic serach later )"""
        conn = get_connection()
        try: 
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM notes WHERE content ILIKE &s ORDER BY created_at DESC",
                    (f"%{query}%",)
                )
                rows = curr.fetchall()
                return [dict(r) for r in rows]
        finally:
            conn.close()