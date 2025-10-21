# trip_planner_app/api_integrations/gen_ai_api.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from django.conf import settings

class GenAIClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gen AI API Key is not set. Please set GEMINI_API_KEY in your .env file.")
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    # *** ADD trip_type TO FUNCTION SIGNATURE ***
    def generate_itinerary(self, budget, starting_point, destination, duration_days,
                          interests, travel_mode_preference, accommodation_preference, food_preference, 
                          trip_type='recreational'): # Default to recreational
        user_preferences = []
        if interests:
            user_preferences.append(f"Interests: {', '.join(interests)}")
        if travel_mode_preference:
            user_preferences.append(f"Preferred travel modes: {', '.join(travel_mode_preference)}")
        if accommodation_preference:
            user_preferences.append(f"Preferred accommodation: {', '.join(accommodation_preference)}")
        if food_preference:
            user_preferences.append(f"Food preferences: {', '.join(food_preference)}")

        preferences_str = "Consider the following preferences: " + "; ".join(user_preferences) + "." if user_preferences else ""
        
        # *** NEW: Tailor prompt based on trip type ***
        if trip_type == 'devotional':
            theme_instruction = (
                "The trip must be COMPLETELY DEVOTIONAL (a pilgrimage). Focus ONLY on temples, sacred sites, shrines, and local rituals. "
                "The activities and attractions must be 100% religious and spiritual in nature. "
                "The food recommendations must prioritize simple, vegetarian, or sattvic food suitable for a pilgrimage. "
                "DO NOT recommend secular tourist spots, restaurants, or bars."
            )
        else:
            theme_instruction = (
                "The trip should be recreational. Focus on sightseeing, adventure, and local cuisine experiences."
            )
        # *** END NEW ***

        prompt = (
            f"{theme_instruction} Generate a personalized, day-wise travel itinerary for a trip from {starting_point} to {destination} "
            f"for {duration_days} days. The total budget for the entire trip is {budget} INR. "
            f"{preferences_str} "
            "For each day, suggest: "
            "1. Best mode of travel within/to the city (e.g., local transport, walking, specific flight/train if inter-city). "
            "2. Accommodation suggestions (within budget). Please provide the exact name and city, in the format: '[Hotel Name (City)]'. "
            "3. Food spots (breakfast, lunch, dinner - within budget). Please provide the exact restaurant name and city, in the format: '[Restaurant Name (City)]'. "
            "4. Tourist attractions/activities (aligning with interests). Please provide the exact attraction name and city, in the format: '[Attraction Name (City)]'. "
            "Ensure the suggestions are within the specified budget and align with the interests and preferences. "
            "Provide the output in a structured, readable Markdown format, clearly separating each day."
            "\n\nExample Day Structure:\n**Day X: [Theme of the day, e.g., Arrival & City Exploration]**\n"
            "* **Travel:** [Details]\n"
            "* **Accommodation:** [Hotel ABC (Moscow)]\n"
            "* **Food:**\n    * Breakfast: [Cafe XYZ (Moscow)]\n    * Lunch: [Restaurant PQR (Moscow)]\n    * Dinner: [Eatery LMN (Moscow)]\n"
            "* **Activities:**\n    * [Red Square (Moscow)]\n    * [St. Basil's Cathedral (Moscow)]\n"
            "\nConclude with a brief budget summary or tip. Ensure all place names and cities are enclosed in brackets like '[Place Name (City)]'."
        )

        try:
            response = self.model.generate_content(prompt)
            itinerary_content = response.text
            return itinerary_content

        except Exception as e:
            print(f"Error generating itinerary with Gen AI: {e}")
            return "Could not generate itinerary. Please try again later. (API Error: Check console for details)"