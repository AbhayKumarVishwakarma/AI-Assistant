from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.llm.groq import get_llm
from app.rag.retriever import get_retriever
from app.prompts.health_prompt import HEALTH_SYSTEM_PROMPT


llm = get_llm()
retriever = get_retriever()

prompt = ChatPromptTemplate.format_messages(
    [
        ("system" , HEALTH_SYSTEM_PROMPT),
        ("human", "{input}")
    ]
)

qa_chain = create_stuff_documents_chain(llm, prompt=prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

def run_health_assistant(query: str):
    """
    Run the RAG chain to answer medical queries using loaded PDFs in Pinecone.
    Returns the answer text.
    """
    try:
        out = rag_chain.invoke({"input": query})
        if isinstance(out, dict):
            for k in ("answer", "output_text", "result", "output"):
                if k in out:
                    return out[k]
            return str(out)
        return str(out)
    except Exception as e:
        return f"Error: {e}"