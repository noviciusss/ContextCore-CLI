import os
import uuid 
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from memory.embeddings import embed_text

load_dotenv()

COLLECTION = os.getenv("COLLECTION_NAME","contextcore_memories")
VECTOR_SIZE = 384 #all-MiniLM-L6-v2 embeddings are 384 dimensional

def get_client():
    return QdrantClient(url=os.getenv("QDRANT_URL"))

def ensure_collection():
    """Create the collections if it doesnot exist yet"""
    client = get_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name = COLLECTION,
            vector_config = VectorParams(size =VECTOR_SIZE,distance = Distance.COSINE)

        )
def write_memory(text:str , metadata: dict = {}):
    """Embed a text snippet """