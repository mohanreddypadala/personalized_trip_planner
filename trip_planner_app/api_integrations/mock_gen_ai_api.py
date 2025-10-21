# trip_planner_app/api_integrations/mock_gen_ai_api.py

import re 

class MockGenAIClient:
    def __init__(self, api_key=None):
        print("--- Using Mock Gen AI Client (API calls are bypassed) ---")

    def generate_itinerary(self, budget, starting_point, destination, duration_days,
                          interests, travel_mode_preference, accommodation_preference, food_preference,
                          trip_type='recreational'): # <-- ADDED trip_type
        
        print(f"Mocking itinerary for: {destination} ({trip_type}) for {duration_days} days with budget {budget}")

        if trip_type == 'devotional':
            mock_itinerary_output = f"""
This is a MOCK DEVOTIONAL itinerary for {destination} (Pilgrimage).

**Day 1: Arrival & Sacred Temple Visit**
* **Travel:** Taxi from {starting_point} to [Tirupati Airport (Tirupati)]. Taxi to accommodation.
* **Accommodation:** [TTD Guest House (Tirupati)] (Simple, devotional stay).
* **Food:**
    * Breakfast: Simple meal/fruits.
    * Lunch: Annadanam at a temple complex (Traditional, Sattvic).
    * Dinner: [Pure Vegetarian Canteen (Tirupati)] (Budget-friendly, simple).
* **Activities:** Check-in. Visit the [Tirumala Temple (Tirupati)] (The main pilgrimage site). Perform the Darshan ritual.

**Day 2: Exploration of Ancient Sites**
* **Travel:** Local bus/Shared cab.
* **Accommodation:** Same as Day 1.
* **Food:**
    * Breakfast: Local South Indian tiffin.
    * Lunch: Temple Prasadam.
    * Dinner: Simple Khichdi at a local ashram.
* **Activities:** Morning: Visit [Sri Padmavathi Ammavari Temple (Tirupati)] (Ancient Shiva Temple). Afternoon: Explore [Kalyani Dam (Tirupati)] (For quiet contemplation). Evening: Participate in evening Aarthi/Bhajan session.

**Budget Summary (Estimate):**
* Flights: 40000 INR
* Accommodation (4 nights): 10000 INR
* Food (Vegetarian/Prasadam): 5000 INR
* Local Transport & Offerings: 5000 INR
**Total: ~60000 INR**
**Note:** This is a strictly vegetarian, pilgrimage-focused itinerary.
"""
        else: # Recreational (Keep your original mock for standard testing)
            mock_itinerary_output = f"""
This is a MOCK RECREATIONAL itinerary for {destination} from the local test client. It focuses on adventure and food, respecting your budget of ₹{budget}.

**Day 1: Arrival in Mumbai & Gateway to India**
* **Travel:** Flight from {starting_point} to [Mumbai Airport (Mumbai)]. Taxi to hotel.
* **Accommodation:** [The Taj Mahal Palace (Mumbai)] (Luxury option, might exceed budget; consider [Hotel Trident (Mumbai)] for mid-range).
* **Food:**
    * Breakfast: Hotel breakfast.
    * Lunch: [Leopold Cafe (Mumbai)] (Iconic, casual dining).
    * Dinner: [Bademiya (Mumbai)] (Street food kebabs, late-night).
* **Activities:** Explore [Gateway of India (Mumbai)], walk along [Marine Drive (Mumbai)], visit [Colaba Causeway (Mumbai)] for shopping.

**Day 2: Bollywood & Beach Vibes**
* **Travel:** Local train/Auto-rickshaw.
* **Accommodation:** Same as Day 1.
* **Food:**
    * Breakfast: Local Vada Pav stall (Mumbai).
    * Lunch: [Pali Village Cafe (Mumbai)] (Bandra, stylish dining).
    * Dinner: Beachside shacks at [Juhu Beach (Mumbai)].
* **Activities:** Morning: Drive past [Mannat (Mumbai)] and [Jalsa (Mumbai)] (Shah Rukh Khan/Amitabh Bachchan's bungalows). Afternoon: Relax at [Juhu Beach (Mumbai)]. Evening: Catch a Bollywood movie at a local cinema.

**Budget Summary (Estimate):**
* Flights: 40000 INR
* Accommodation (4 nights): 30000 INR (Adjust based on choice)
* Food: 20000 INR
* Local Transport & Activities: 10000 INR
**Total: ~100000 INR**
"""
        return mock_itinerary_output