from langchain_tavily import TavilySearch
from langchain.tools import Tool
from app.llm.groq import get_llm
from app.config import TAVILY_API_KEY
from app.prompts.system_prompts import MY_AGENT_SYSTEM


search = TavilySearch(max_results=5)

def summarize(query: str, raw: str):
    llm = get_llm()

    prompt = (
        f"Question: {query}\n"
        f"Search results: {raw}\n"
        f"{MY_AGENT_SYSTEM}"
    )

    try:
        out = llm.invoke(prompt)
        if hasattr(out, "content"):
            return out.content.strip()
        return str(out).strip()
    except Exception as e:
        return f"Error summarizing: {str(e)}"
    

def search_and_summarize(query: str) -> str:
    try:
        raw = search.run(query)
        return summarize(query, raw)
    except Exception as e:
        return f"Error searching and summarizing: {str(e)}"
    
def get_search_tool():
    return Tool(
        name="web_search",
        func=search_and_summarize,
        description="Use to search the web and return a concise direct answer."
    )