import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from app.rag.loader import load_documents, filter_to_minimal_docs
from app.rag.vectorstore import get_or_create_index
from app.llm.embeddings import get_embedding
from app.config import PINECONE_INDEX

def ingest_pdf_to_pinecone(pdf_dir: str, index_name: str):
    """
    Load PDFs from a directory, embed them, and store in Pinecone.
    """

    print(f"Loading PDFs from: {pdf_dir}")
    docs = load_documents(pdf_dir)
    docs = filter_to_minimal_docs(docs)

    if not docs:
        print("No PDF documents found!")
        return
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embedding = get_embedding()
    get_or_create_index(index_name, dim=384)
    
    print(f"⬆️ Uploading {len(chunks)} chunks into Pinecone index: {index_name}")

    PineconeVectorStore.from_documents(chunks, embedding, index_name=index_name)

    print("Data is now stored in Pinecone!")


if __name__ == "__main__":
    ingest_pdf_to_pinecone(pdf_dir="data/", index_name=PINECONE_INDEX)