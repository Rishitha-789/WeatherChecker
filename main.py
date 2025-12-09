from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from weather_api import get_current_weather, get_forecast
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load city data for autocomplete
with open("data/cities.json", "r") as f:
    cities = json.load(f)

recent_searches = []

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# JSON endpoint for weather
@app.get("/weather_json")
def weather_json(city: str = "", units: str = "metric"):
    global recent_searches
    weather_data = get_current_weather(city, units)
    forecast_data = get_forecast(city, units) if "error" not in weather_data else None

    # Update recent searches
    if "error" not in weather_data:
        recent_searches = [city] + [c for c in recent_searches if c != city]
        recent_searches = recent_searches[:5]

    return JSONResponse(content={
        "weather": weather_data,
        "forecast": forecast_data,
        "recent": recent_searches
    })

# Autocomplete endpoint
@app.get("/autocomplete")
def autocomplete(q: str):
    suggestions = [c for c in cities if c.lower().startswith(q.lower())][:5]
    return JSONResponse(content=suggestions)
