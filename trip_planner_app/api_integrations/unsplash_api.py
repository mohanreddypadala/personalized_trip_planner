# trip_planner_app/api_integrations/unsplash_api.py
import requests
import os
# --- CRITICAL FIX: Import settings here so it's globally available to the module ---
from django.conf import settings 
# ---------------------------------------------------------------------------------

class UnsplashAPIClient:
    def __init__(self, access_key):
        if not access_key:
            print("Warning: Unsplash ACCESS KEY is missing.")
        self.access_key = access_key
        self.base_url = "https://api.unsplash.com/search/photos"

    def search_image(self, query, orientation='landscape', count=1):
        """Fetches a relevant image URL from Unsplash based on a query."""
        
        # --- OFFLINE/MOCK CHECK ---
        # The variables settings.USE_MOCK_AI_CLIENT and settings.DEBUG are now correctly available.
        if not self.access_key or settings.USE_MOCK_AI_CLIENT:
            # If in mock mode or key is missing, return a placeholder.
            if settings.DEBUG: # Only return placeholder in debug/dev mode
                return "https://via.placeholder.com/600x400?text=Image+Placeholder"
            return None

        headers = {
            "Authorization": f"Client-ID {self.access_key}"
        }
        params = {
            "query": query,
            "orientation": orientation,
            "per_page": count,
            "content_filter": "high"
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=5) 
            response.raise_for_status()
            data = response.json()
            
            if data and data['results']:
                return data['results'][0]['urls']['small']
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from Unsplash for query '{query}': {e}")
            return None