# Voice-Based Location Chatbot (Backend)

This Flask backend handles location-based queries like fuel stations, hotels, toilets, weather, etc.

## How to Run

1. Install dependencies:
    pip install -r requirements.txt

2. Add your Google Maps & OpenWeatherMap API keys in `app.py`.

3. Run the server:
    python app.py

## API Endpoint

POST `/chat`

Request JSON:
```json
{
  "query": "fuel near me",
  "latitude": 12.9716,
  "longitude": 77.5946
}
