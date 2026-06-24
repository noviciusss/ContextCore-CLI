#pyrefly: ignore
from sentence_transformers import SentenceTransformer

#loaded once ,reused  - loading is slow , inference is fast
_model  = None

def get_embedding_model():
    global _model 
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model 

def embed_text(text:str)->list[float]:
    model = get_embedding_model()
    return model.encode(text).tolist() # tolist() -> converts numpy array -> plain python list ehich qdrant expects 
    