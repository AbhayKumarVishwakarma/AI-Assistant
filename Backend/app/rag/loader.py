from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.schema import Document
from typing import List


def load_documents(directory_path: str) -> List[Document]:
    """
    Load all PDFs from the given directory and return a list of Documents.
    """
    loader = DirectoryLoader(directory_path, glob="*.pdf", loader_cls=PyPDFLoader)
    doc = loader.load()
    return doc


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal = []

    for d in docs:
        src = d.metadata.get("source")
        minimal.append(Document(page_content=d.page_content, metadata={"source": src}))

    return minimal
