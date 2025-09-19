import os
import google.generativeai as genai
from dotenv import load_dotenv

class GenAIClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gen AI API Key is not set. Please set GEN_AI_API_KEY in your .env file.")
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using a currently supported model

    def generate_itinerary(self, budget, starting_point, destination, duration_days,
                          interests, travel_mode_preference, accommodation_preference, food_preference):
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

        # --- MODIFIED PROMPT HERE ---
        # Explicitly asking for specific formats like "[Place Name (City)]" for easier parsing.
        prompt = (
            f"Generate a personalized, day-wise travel itinerary for a trip from {starting_point} to {destination} "
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

# Example for testing within this file (remove or comment out in production)
if __name__ == '__main__':
    load_dotenv() # Ensure .env is loaded for standalone execution
    api_key_from_env = os.getenv("GEN_AI_API_KEY")

    if api_key_from_env:
        try:
            client = GenAIClient(api_key_from_env)
            print("--- Listing available Gemini models that support 'generateContent' ---")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"Model Name: {m.name}, Display Name: {m.display_name}")

            print("\n--- Attempting a test itinerary generation with 'gemini-1.5-flash' ---")
            test_itinerary = client.generate_itinerary(
                budget=50000,
                starting_point="Vijayawada, India",
                destination="Goa, India",
                duration_days=5,
                interests=['nature', 'foodie'],
                travel_mode_preference=['flight'],
                accommodation_preference=['hotel'],
                food_preference=['local', 'seafood']
            )
            print("\nTest Itinerary (first 500 chars):\n", test_itinerary[:500], "...")

        except ValueError as e:
            print(f"Configuration Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during test: {e}")
    else:
        print("GEN_AI_API_KEY not found in .env. Please ensure it is set correctly in your project root.")