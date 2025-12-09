import requests
from datetime import datetime

# OpenWeather API key and base URL
API_KEY = "ecc57cf145c51184d56311878e9f6986"
BASE_URL = "https://api.openweathermap.org/data/2.5"
# get current weather function
def get_current_weather(city: str, units: str = "metric"):
    """
    Fetch current weather for a city.
    Returns dict with city, temp, humidity, description, icon, wind, lat, lon.
    """
    try:
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={units}"
        response = requests.get(url, timeout=10).json()

        if response.get("cod") != 200:
            return {"error": response.get("message", "City not found")}

        return {
            "city": response["name"],
            "temp": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "description": response["weather"][0]["description"].title(),
            "icon": response["weather"][0]["icon"],
            "wind": response["wind"]["speed"],
            "lat": response["coord"]["lat"],
            "lon": response["coord"]["lon"],
        }

    except requests.exceptions.RequestException:
        return {"error": "Network error. Try again."}
    except Exception:
        return {"error": "Unexpected error. Please try later."}

# Forecast function
def get_forecast(city: str, units: str = "metric"):
    """
    Fetch 5-day forecast (3-hour intervals) and aggregate into daily min/max.
    Returns list of daily summaries (up to 7 days) with Unix timestamps.
    """
    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={units}"
        response = requests.get(url, timeout=10).json()

        if response.get("cod") != "200":
            return {"error": response.get("message", "Could not fetch forecast")}

        daily = {}
        for item in response["list"]:
            date_obj = datetime.fromtimestamp(item["dt"])
            date_key = date_obj.date()  # just the day

            if date_key not in daily:
                daily[date_key] = {
                    "date": int(date_obj.timestamp()),   # Unix timestamp
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"],
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"]
                }
            else:
                daily[date_key]["temp_min"] = min(daily[date_key]["temp_min"], item["main"]["temp_min"])
                daily[date_key]["temp_max"] = max(daily[date_key]["temp_max"], item["main"]["temp_max"])

        forecast = []
        for i, (date_key, data) in enumerate(daily.items()):
            if i >= 7:
                break
            forecast.append(data)

        return forecast

    except requests.exceptions.RequestException:
        return {"error": "Network error. Try again."}
    except Exception:
        return {"error": "Unexpected error. Please try later."}
