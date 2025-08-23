from langchain.agents import initialize_agent, AgentType
from app.llm.groq import get_llm
from app.memory.memory import get_memory
from app.tools.search import get_search_tool
from app.tools.weather import get_weather


llm = get_llm()
tools = [get_search_tool(), get_weather]
memory = get_memory()


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False
)


def run_agent(query: str):
    try:
        resp = agent.run(query)
        return resp
    except Exception as e:
        return f"Error running agent: {str(e)}"