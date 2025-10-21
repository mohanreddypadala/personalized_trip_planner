from django import forms

class TripPlanningForm(forms.Form):
    budget = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label="Your Budget (in your local currency, e.g., INR)",
        help_text="e.g., 50000.00"
    )
    trip_type = forms.CharField(widget=forms.HiddenInput(), required=False) 
    
    budget = forms.DecimalField(
        # ... (rest of budget field definition) ...
    )
    starting_point = forms.CharField(
        max_length=255,
        label="Starting Point (City, Country)",
        help_text="e.g., Vijayawada, India"
    )
    destination = forms.CharField(
        max_length=255,
        label="Destination (City, Country)",
        help_text="e.g., Goa, India or Paris, France"
    )
    trip_duration_days = forms.IntegerField(
        min_value=1,
        max_value=30, # Max duration to prevent excessively long plans
        label="Trip Duration (Days)",
        help_text="e.g., 5"
    )
    # Add other preferences like "Interests" (e.g., 'adventure', 'history', 'foodie')
    interests = forms.MultipleChoiceField(
        choices=[
            ('adventure', 'Adventure & Outdoors'),
            ('history', 'History & Culture'),
            ('foodie', 'Food & Drink'),
            ('nature', 'Nature & Scenic'),
            ('shopping', 'Shopping & Lifestyle'),
            ('relaxation', 'Relaxation & Wellness'),
            ('nightlife', 'Nightlife & Entertainment'),
            ('family', 'Family-Friendly'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Interests (Optional)",
        help_text="Select all that apply."
    )
    travel_mode_preference = forms.MultipleChoiceField(
        choices=[
            ('flight', 'Flight'),
            ('train', 'Train'),
            ('bus', 'Bus'),
            ('car', 'Car/Self-drive'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Preferred Travel Modes (Optional)",
        help_text="How do you prefer to travel between cities/major points?"
    )
    accommodation_preference = forms.MultipleChoiceField(
        choices=[
            ('hotel', 'Hotel'),
            ('hostel', 'Hostel'),
            ('guesthouse', 'Guesthouse/B&B'),
            ('resort', 'Resort'),
            ('apartment', 'Apartment/Vacation Rental'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Preferred Accommodation Types (Optional)",
        help_text="What kind of place do you like to stay in?"
    )
    food_preference = forms.MultipleChoiceField(
        choices=[
            ('local', 'Local Cuisine'),
            ('fine_dining', 'Fine Dining'),
            ('casual', 'Casual Dining'),
            ('vegetarian', 'Vegetarian/Vegan Friendly'),
            ('street_food', 'Street Food'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Food Preferences (Optional)",
        help_text="Any specific dining experiences you're looking for?"
    )