# trip_planner_app/views.py

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from .forms import TripPlanningForm
from .api_integrations.gen_ai_api import GenAIClient
# from .api_integrations.travel_api import TravelAPIClient # Uncomment when integrated
# from .api_integrations.accommodation_api import AccommodationAPIClient # Uncomment when integrated
# from .api_integrations.attractions_api import AttractionsAPIClient # Uncomment when integrated
# from .api_integrations.food_api import FoodAPIClient # Uncomment when integrated

from .utils.pdf_generator import generate_itinerary_pdf

import markdown
import re
import urllib.parse # For URL encoding

# Helper function to generate Google Maps and Hotel Search URLs for HTML display
def generate_place_links(text, destination_city=""):
    # Regex to find names in format [Name (City)] or [Name (Some Place)]
    pattern = re.compile(r'\[([^\]]+?)\s*\(?([A-Za-z\s,-]*?)?\)?\]')

    def replace_with_link(match):
        place_name = match.group(1).strip()
        city = match.group(2).strip() if match.group(2) else destination_city

        city_for_url = city.split(',')[0].strip() if city else ""

        # Using the standard Google Maps search URL format
        maps_query = urllib.parse.quote_plus(f"{place_name}, {city_for_url}")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}" 

        # Generic Hotel/Restaurant Search URL (Google Search will link to booking sites)
        if "hotel" in place_name.lower() or "resort" in place_name.lower() or "guesthouse" in place_name.lower() or "stay" in place_name.lower() or "inn" in place_name.lower():
            booking_query = urllib.parse.quote_plus(f"{place_name} {city_for_url} booking")
            booking_url = f"https://www.google.com/search?q={booking_query}"
            return f'<a href="{maps_url}" target="_blank">{place_name} <i class="bi bi-geo-alt-fill"></i></a> <small>(<a href="{booking_url}" target="_blank">Book <i class="bi bi-box-arrow-up-right"></i></a>)</small>'
        else: # Assume it's an attraction or food spot
            return f'<a href="{maps_url}" target="_blank">{place_name} <i class="bi bi-geo-alt-fill"></i></a>'

    processed_text = pattern.sub(replace_with_link, text)
    return processed_text

def plan_trip_view(request):
    itinerary_text = None
    pdf_download_url = None
    itinerary_html = None

    if request.method == 'POST':
        form = TripPlanningForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            starting_point = form.cleaned_data['starting_point']
            destination = form.cleaned_data['destination']
            trip_duration_days = form.cleaned_data['trip_duration_days']
            interests = form.cleaned_data['interests']
            travel_mode_preference = form.cleaned_data['travel_mode_preference']
            accommodation_preference = form.cleaned_data['accommodation_preference']
            food_preference = form.cleaned_data['food_preference']

            try:
                gen_ai_client = GenAIClient(settings.GEN_AI_API_KEY)
                itinerary_text = gen_ai_client.generate_itinerary(
                    budget=budget,
                    starting_point=starting_point,
                    destination=destination,
                    duration_days=trip_duration_days,
                    interests=interests,
                    travel_mode_preference=travel_mode_preference,
                    accommodation_preference=accommodation_preference,
                    food_preference=food_preference
                )
                if not itinerary_text or "Could not generate itinerary" in itinerary_text:
                    messages.error(request, "Failed to generate itinerary. Please try again or refine your input.")
                    itinerary_text = None
            except Exception as e:
                messages.error(request, f"An error occurred while communicating with the AI: {e}. Please check your API key and model availability.")
                itinerary_text = None

            if itinerary_text:
                destination_city_only = destination.split(',')[0].strip()

                # Process the AI text to add links for HTML display
                itinerary_text_with_links_html_ready = generate_place_links(itinerary_text, destination_city_only)

                # Convert Markdown with embedded links to HTML for display on the webpage
                itinerary_html = markdown.markdown(itinerary_text_with_links_html_ready)

                # Store original Markdown for PDF generation (PDF generation will re-parse for its format)
                request.session['itinerary_data_for_pdf'] = {
                    'budget': float(budget),
                    'starting_point': starting_point,
                    'destination': destination,
                    'trip_duration_days': trip_duration_days,
                    'interests': interests,
                    'travel_mode_preference': travel_mode_preference,
                    'accommodation_preference': accommodation_preference,
                    'food_preference': food_preference,
                    'itinerary_content': itinerary_text # Store original Markdown for PDF processing
                }
                pdf_download_url = '/plan/download-itinerary-pdf/'
        else:
            messages.error(request, "Please correct the errors in your input.")

    else:
        form = TripPlanningForm()

    context = {
        'form': form,
        'itinerary_text': itinerary_text, # Keep for debugging or remove
        'itinerary_html': itinerary_html,
        'pdf_download_url': pdf_download_url
    }
    return render(request, 'trip_planner_app/plan_trip.html', context)

def download_itinerary_pdf_view(request):
    itinerary_data = request.session.get('itinerary_data_for_pdf')
    if not itinerary_data:
        messages.error(request, "No itinerary data found to generate PDF. Please generate a plan first.")
        return HttpResponse("No itinerary data found. Please generate a plan first.", status=404)

    try:
        pdf_buffer = generate_itinerary_pdf(itinerary_data)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="personalized_trip_itinerary.pdf"'
        return response
    except Exception as e:
        import traceback
        traceback.print_exc() # IMPORTANT: This prints the full Python traceback to your console!
        messages.error(request, f"Error generating PDF: {e}. Please check server console for details.")
        return HttpResponse(f"Error generating PDF. Please try again. ({e})", status=500)