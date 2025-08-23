from langchain_pinecone import PineconeVectorStore
from app.llm.embeddings import get_embedding
from app.config import PINECONE_INDEX


def get_retriever():
    embedding = get_embedding()
    vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embedding)
    return vectorstore.as_retriever() 