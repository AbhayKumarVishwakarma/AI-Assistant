from langchain_huggingface import HuggingFaceEmbeddings

embedding = None

def get_embedding():
    global embedding
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    if embedding is None:
        embedding = HuggingFaceEmbeddings(model_name=model_name)
    return embedding