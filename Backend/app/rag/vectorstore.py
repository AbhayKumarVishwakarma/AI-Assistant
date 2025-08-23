from pinecone import Pinecone, ServerlessSpec
from app.config import PINECONE_API_KEY, PINECONE_ENV 


pc = Pinecone(api_key=PINECONE_API_KEY)


def get_or_create_index(idx_name: str, dim: int = 384, metric: str = "cosine"):
    
    if not pc.has_index(idx_name):
        pc.create_index(
            name=idx_name,
            dimension=dim,
            metric=metric,
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV or "us-east-1"),
        )

    return pc.Index(idx_name)
