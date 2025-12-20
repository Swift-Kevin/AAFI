from typing import Dict
import httpx

USER_AGENT = "myweatherapp.com, contact@myweatherapp.com"

async def findlatlon(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, headers=headers, timeout=500)
            resp.raise_for_status()
        except Exception as e:
            print(f"Nominatim request failed: {e}")
            return None, None

        try:
            data = resp.json()
        except Exception as e:
            print(f"JSON decode error from Nominatim: {e}")
            return None, None

    if not data:
        return None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon

async def get_weather_nws(lat: float, lon: float):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    lat = round(lat, 4)
    lon = round(lon, 4)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            point_resp = await client.get(f"https://api.weather.gov/points/{lat},{lon}", headers=headers, timeout=500)
            point_resp.raise_for_status()
            point_data = point_resp.json()
            forecast_url = point_data["properties"]["forecast"]
        except Exception as e:
            print(f"NWS points request failed: {e}")
            return {"name": "", "temperature": "N/A", "forecast": "Unable to fetch weather"}

        try:
            forecast_resp = await client.get(forecast_url, headers=headers, timeout=500)
            forecast_resp.raise_for_status()
            forecast_data = forecast_resp.json()
            today_forecast = forecast_data["properties"]["periods"][0]
        except Exception as e:
            print(f"NWS forecast request failed: {e}")
            return {"name": "", "temperature": "N/A", "forecast": "Unable to fetch weather"}

    return {
        "name": today_forecast["name"],
        "temperature": f"{today_forecast['temperature']} {today_forecast['temperatureUnit']}",
        "forecast": today_forecast["detailedForecast"]
    }

async def get_weather(city: str) -> Dict:
    lat, lon = await findlatlon(city)
    if lat is None or lon is None:
        return {"city": city, "forecast": "Unknown city", "temperature": "N/A"}

    weather = await get_weather_nws(lat, lon)
    weather["city"] = city
    return weather




FAQ_KB = {
    "hours": "Our office hours are 9am-5pm, Monday to Friday.",
    "location": "We are located at 123 Main Street.",
    "support": "You can contact support at support@example.com."
}

def lookup_kb(query: str) -> Dict:
    for key, answer in FAQ_KB.items():
        if key in query.lower():
            return {"query": query, "answer": answer}
    return {"query": query, "answer": "Sorry, I don't know."}


GEODB_API_KEY = "df60d96811msh3f3730a00fdcd4cp12061ajsnf84bfe2d80a7"
GEODB_HOST = "wft-geo-db.p.rapidapi.com"

async def get_population(city: str) -> Dict:
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    headers = {
        "X-RapidAPI-Key": GEODB_API_KEY,
        "X-RapidAPI-Host": GEODB_HOST
    }
    params = {"namePrefix": city, "limit": 1, "sort": "-population"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        data = resp.json()

    if data.get("data"):
        city_data = data["data"][0]
        population = city_data.get("population", "unknown")
        city_name = city_data.get("name", city)
        return {"city": city_name, "population": population}
    else:
        return {"city": city, "population": "unknown"}


stored_tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "lookup_kb",
        "description": "Search local knowledge base (FAQ)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Question to lookup"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_population",
        "description": "Finds the population of a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Name of the city"}
            },
            "required": ["city"]
        }
    }
]