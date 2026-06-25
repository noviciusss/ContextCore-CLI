import os
import uuid 
#pyrefly:ignore 
from dotenv import load_dotenv
#pyrefly:ignore 
from qdrant_client import QdrantClient
#pyrefly:ignore
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
    """Embed a text snippet and store in Qdrant."""
    client  = get_client()
    ensure_collection()
    vector  = embed_text(text)
    point  = PointStruct(
        id = str(uuid.uuid4()), # qdrant requires every stored point to have a unique id 
        vector = vector,
        payload = {"text": text, **metadata}
    )
    client.upsert(collection_name = COLLECTION,points=[point])

def search_memory(query:str,top_k : int=3) ->list[str]:
    """Find too_k most sementically similar past memories to the query"""
    client = get_client()
    ensure_collection()
    query_vector = embed_text(query)
    results = client.search(
        collection_name = COLLECTION,
        query_vector = query_vector,
        limit = top_k
    )
    return [hit.payload["text"] for hit in results]
