import json

# ── Tool Functions ────────────────────────────────

def search_flights(origin: str, destination: str, date: str = "2025-08-01") -> str:
    """Search for available flights between two cities."""
    return json.dumps({
        "route":   f"{origin} → {destination}",
        "date":    date,
        "flights": [
            {"id": "F001", "airline": "Qantas",            "price": "$850",  "dep": "08:00", "dur": "8h"},
            {"id": "F002", "airline": "Singapore Airlines", "price": "$720",  "dep": "11:00", "dur": "9h"},
            {"id": "F003", "airline": "Emirates",           "price": "$1100", "dep": "18:00", "dur": "7h"},
        ]
    })


def search_hotels(city: str, guests: int = 2) -> str:
    """Search for hotels in a city."""
    return json.dumps({
        "city":   city,
        "guests": guests,
        "hotels": [
            {"id": "H001", "name": f"{city} Grand Hotel",   "price": "$150/night", "rating": "4.8 ⭐"},
            {"id": "H002", "name": f"{city} Luxury Resort", "price": "$300/night", "rating": "4.9 ⭐"},
            {"id": "H003", "name": f"{city} Budget Inn",    "price": "$75/night",  "rating": "4.2 ⭐"},
        ]
    })


def get_weather(city: str) -> str:
    """Get current weather for a city."""
    data = {
        "tokyo":    {"temp": "22°C", "condition": "Sunny",        "humidity": "65%", "wind": "12 km/h"},
        "sydney":   {"temp": "18°C", "condition": "Partly Cloudy","humidity": "75%", "wind": "15 km/h"},
        "london":   {"temp": "12°C", "condition": "Rainy",        "humidity": "85%", "wind": "20 km/h"},
        "dubai":    {"temp": "38°C", "condition": "Hot & Sunny",  "humidity": "40%", "wind": "8 km/h"},
        "paris":    {"temp": "16°C", "condition": "Cloudy",       "humidity": "70%", "wind": "18 km/h"},
        "new york": {"temp": "15°C", "condition": "Windy",        "humidity": "70%", "wind": "25 km/h"},
        "bali":     {"temp": "29°C", "condition": "Tropical",     "humidity": "80%", "wind": "10 km/h"},
    }
    info = data.get(city.lower(), {"temp": "25°C", "condition": "Clear", "humidity": "60%", "wind": "10 km/h"})
    return json.dumps({"city": city, **info})


def book_flight(destination: str, date: str, passenger: str) -> str:
    """Book a flight to a destination."""
    return json.dumps({
        "status":       "Confirmed ✅",
        "confirmation": "CONF-AZ-2025-XYZ",
        "destination":  destination,
        "date":         date,
        "passenger":    passenger,
        "price":        "$850",
        "seat":         "14A (Window)",
        "message":      "Your flight has been booked! Check email for details."
    })


def get_destination_info(destination: str) -> str:
    """Get travel information about a destination."""
    info = {
        "tokyo":  {"country": "Japan",     "currency": "JPY", "language": "Japanese", "visa": "Visa-free (90 days)", "best_time": "Mar-May, Oct-Nov", "avg_cost": "$120/day"},
        "sydney": {"country": "Australia", "currency": "AUD", "language": "English",  "visa": "eVisitor required",   "best_time": "Sep-Nov, Mar-May", "avg_cost": "$130/day"},
        "london": {"country": "UK",        "currency": "GBP", "language": "English",  "visa": "ETA required",        "best_time": "Jun-Aug",          "avg_cost": "$150/day"},
        "dubai":  {"country": "UAE",       "currency": "AED", "language": "Arabic",   "visa": "Visa on arrival",     "best_time": "Nov-Mar",          "avg_cost": "$200/day"},
        "paris":  {"country": "France",    "currency": "EUR", "language": "French",   "visa": "Schengen visa",       "best_time": "Apr-Jun, Sep-Oct", "avg_cost": "$160/day"},
        "bali":   {"country": "Indonesia", "currency": "IDR", "language": "Balinese", "visa": "Visa on arrival",     "best_time": "Apr-Oct",          "avg_cost": "$60/day"},
    }
    result = info.get(destination.lower(), {"message": f"No specific info available for {destination}"})
    return json.dumps({"destination": destination, **result})


# ── Tool Schemas ──────────────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name":        "search_flights",
            "description": "Search for available flights between two cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin":      {"type": "string", "description": "Origin city name"},
                    "destination": {"type": "string", "description": "Destination city name"},
                    "date":        {"type": "string", "description": "Travel date in YYYY-MM-DD format"},
                },
                "required": ["origin", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":        "search_hotels",
            "description": "Search for available hotels in a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city":   {"type": "string",  "description": "City to search hotels in"},
                    "guests": {"type": "integer", "description": "Number of guests"},
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":        "get_weather",
            "description": "Get current weather conditions for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":        "book_flight",
            "description": "Book a flight to a destination on a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "Destination city"},
                    "date":        {"type": "string", "description": "Travel date YYYY-MM-DD"},
                    "passenger":   {"type": "string", "description": "Passenger full name"},
                },
                "required": ["destination", "date", "passenger"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name":        "get_destination_info",
            "description": "Get travel information, visa requirements, and tips for a destination",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "Destination city or country"},
                },
                "required": ["destination"]
            }
        }
    },
]


def execute_tool(name: str, args: dict) -> str:
    """Execute a tool by name with given arguments."""
    mapping = {
        "search_flights":      search_flights,
        "search_hotels":       search_hotels,
        "get_weather":         get_weather,
        "book_flight":         book_flight,
        "get_destination_info": get_destination_info,
    }
    fn = mapping.get(name)
    if fn:
        return fn(**args)
    return json.dumps({"error": f"Unknown tool: {name}"})
