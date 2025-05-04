from flask import Flask, request, jsonify
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # 👈 This line enables CORS

MAPBOX_API_KEY = "pk.eyJ1IjoiYXJ1bGVlc3dhcmFuIiwiYSI6ImNtOXBpZWViczEzc3kya3NldHp6Mm14cDEifQ.3Yl29UBAS5KHEC9xWCYO3A"
WEATHER_API_KEY = "dc6570fdefd02dcceb5465a24a89af9e"

# Intent keyword mapping
intent_map = {
    "fuel": ["fuel", "petrol", "gas", "petrol pump", "fuel station", "gas station"],
    "hotel": ["hotel", "lodge", "stay", "accommodation"],
    "toilet": ["toilet", "washroom", "restroom", "bathroom"],
    "mechanic": ["mechanic", "repair", "garage", "car repair"],
    "cafe": ["cafe", "coffee", "tea shop"],
    "restaurant": ["restaurant", "food", "eatery", "dining"],
    "ev": ["ev", "charging", "charging station", "electric vehicle"],
    "parking": ["parking", "park my car", "parking spot"]
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get("query", "").lower()
    lat = data.get("latitude")
    lng = data.get("longitude")

    if not query or not lat or not lng:
        return jsonify({"response": "Please provide a valid query and location."}), 400

    if "weather" in query:
        return get_weather(lat, lng)
    else:
        return get_places(query, lat, lng)

def get_intent(query):
    for intent, keywords in intent_map.items():
        for word in keywords:
            if word in query:
                return intent
    return "rest stop"

def get_places(query, lat, lng):
    intent = get_intent(query)

    # Use Mapbox Search API for finding places
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{intent}.json?proximity={lng},{lat}&access_token={MAPBOX_API_KEY}"
    response = requests.get(url).json()

    if not response["features"]:
        return jsonify({"response": f"No nearby {intent}s found."})

    place = response["features"][0]
    name = place["text"]
    address = place.get("place_name", "Address not available")
    directions_link = f"https://www.google.com/maps/dir/?api=1&destination={place['geometry']['coordinates'][1]},{place['geometry']['coordinates'][0]}"

    reply = f"The nearest {intent} is {name}, located at {address}. Here's the directions link."

    return jsonify({
        "response": reply,
        "directions": directions_link
    })

def get_weather(lat, lng):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={WEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("main"):
        temp = data["main"]["temp"]
        cond = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        response = f"The current temperature is {temp}°C with {cond}. Humidity is {humidity}% and wind speed is {wind} m/s."
        return jsonify({"response": response})

    return jsonify({"response": "Unable to fetch weather details."})

if __name__ == "__main__":
    app.run(debug=True)
