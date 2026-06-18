import psycopg2
import os 
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
def get_connection():
    return psycopg2.connect(os.get("POSTGRES_URL"),cursor_factory=RealDictCursor)