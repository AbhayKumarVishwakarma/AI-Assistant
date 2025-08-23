import requests
from langchain.tools import tool
from app.config import OPENWEATHER_API_KEY

@tool
def get_weather(city: str) -> str:
    """
    Fetch current weather for a given city using OpenWeather API.
    Returns a concise direct answer (no meta commentary).
    """
    
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key not configured."
    
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
    except Exception as e:
        return f"Weather fetch error: {e}"
    
    if data.get("cod") != 200:
        return f"Error: {data.get('message', 'failed to fetch weather')}"
    
    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    
    return f"{city}: {weather}, {temp}°C."