import psycopg2
import os 
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("POSTGRES_URL"), cursor_factory=RealDictCursor)

def init_db():
    """Initializes the database schema using init_db.sql"""
    sql_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
    if not os.path.exists(sql_path):
        return
    with open(sql_path, "r") as f:
        sql = f.read()
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    finally:
        conn.close()