# trip_planner_app/api_integrations/opentripmap_api.py
import requests
from django.conf import settings

class OpenTripMapClient:
    def __init__(self, api_key):
        self.api_key = api_key
        # Note: The API key for OTM is often passed in the query params.
        self.base_url = "http://api.opentripmap.com/0.1/en/places/"

    def get_coordinates(self, city_name):
        """Fetches lat/lon for a given city name."""
        # --- OFFLINE/MOCK CHECK ---
        if not self.api_key or settings.USE_MOCK_AI_CLIENT:
            # Return fixed mock coordinates for testing functionality
            return 77.0, 28.0 # Mock coords for Delhi
        
        url = self.base_url + "geoname"
        params = {
            "name": city_name,
            "apikey": self.api_key
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            # OTM returns a list; we take the first valid result
            if data and data.get('name', '').lower() == city_name.lower():
                return data['lon'], data['lat']
            return None, None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching coordinates for {city_name}: {e}")
            return None, None

    def search_devotional_pois(self, lon, lat, radius=10000, limit=5):
        """Searches for Temples, Churches, Shrines near coordinates."""
        if not self.api_key or settings.USE_MOCK_AI_CLIENT:
            return {"features": [{"properties": {"name": "Mock Temple Site"}},
                                 {"properties": {"name": "Mock Shrine"}},]} # Mock POIs

        # Kinds for devotional: religion is the general category
        kinds = "churches,temples,monasteries,shrines,stupa,mosques"
        url = self.base_url + "radius"
        params = {
            "radius": radius, # 10 km radius
            "lon": lon,
            "lat": lat,
            "kinds": kinds,
            "limit": limit,
            "apikey": self.api_key
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching devotional POIs: {e}")
            return {"features": []}