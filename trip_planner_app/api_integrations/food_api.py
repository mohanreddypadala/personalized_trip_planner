import requests
import json

class FoodAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        # Replace with actual base URL (e.g., Yelp Fusion API, Zomato/Swiggy API - though these are often for delivery)
        self.base_url = "https://api.foodservice.com/v1" # This is a placeholder
        self.headers = {
            "Authorization": f"Bearer {self.api_key}", # Check specific API docs for auth method
            "Content-Type": "application/json"
        }
        # Note: You'll need to implement actual API calls based on the chosen provider's documentation.

    def search_restaurants(self, location, query=None, categories=None, price_tier=None, sort_by='rating', limit=10):
        """
        Searches for restaurants.
        `location` could be city or lat/lon.
        `categories` could be 'indian', 'italian', 'cafe', 'vegetarian'.
        `price_tier` can be 1, 2, 3, 4 (e.g., $, $$, $$$, $$$$).
        """
        endpoint = f"{self.base_url}/restaurants/search"
        params = {
            "location": location,
            "limit": limit,
            "sortBy": sort_by,
            "apiKey": self.api_key # Some APIs use query param for key, others use headers
        }
        if query:
            params["term"] = query # e.g., "pizza"
        if categories:
            params["categories"] = ",".join(categories)
        if price_tier:
            params["price"] = price_tier

        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching restaurants: {e}")
            return None