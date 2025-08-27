from dotenv import load_dotenv
import os

load_dotenv()

# Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Search (Tavily)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# OpenWeather
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Pinecone Vector DB
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "health-assistance")
PINECONE_ENV = os.getenv("PINECONE_ENV", "")

# MongoDB 
MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("DB_NAME", "")
SECRET_KEY = os.getenv("SECRET_KEY", "LOISHDFT443OHNP443JHOI93LHOIH3HOSFD9369LH")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

