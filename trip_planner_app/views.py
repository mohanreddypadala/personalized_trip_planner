# trip_planner_app/views.py

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from .forms import TripPlanningForm

# --- CRITICAL IMPORTS ---
from .api_integrations.gen_ai_api import GenAIClient
from .api_integrations.unsplash_api import UnsplashAPIClient 
from .api_integrations.mock_gen_ai_api import MockGenAIClient
from .utils.pdf_generator import generate_itinerary_pdf
from .utils.itinerary_parser import parse_ai_itinerary_to_structure 
# --- END CRITICAL IMPORTS ---

import re
import urllib.parse 

# =============================================================
# HELPER FUNCTION FOR HTML LINK GENERATION
# =============================================================

def generate_place_links_html(text_segment, destination_city=""):
    """
    Converts [Place (City)] patterns in raw text into clickable HTML links 
    for the web display, adding Bootstrap icons.
    """
    pattern = re.compile(r'\[([^\]]+?)\s*\(?([A-Za-z\s,-]*?)?\)?\]')

    def replace_with_link(match):
        place_name = match.group(1).strip()
        city = match.group(2).strip() if match.group(2) else destination_city

        city_for_url = city.split(',')[0].strip() if city else ""

        maps_query = urllib.parse.quote_plus(f"{place_name}, {city_for_url}")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

        if any(x in place_name.lower() for x in ["hotel", "resort", "guesthouse", "stay", "inn"]):
            booking_query = urllib.parse.quote_plus(f"{place_name} {city_for_url} hotel booking")
            booking_url = f"https://www.google.com/search?q={booking_query}"
            return f'<a href="{maps_url}" target="_blank">{place_name} <i class="bi bi-geo-alt-fill"></i></a> <small>(<a href="{booking_url}" target="_blank">Book <i class="bi bi-box-arrow-up-right"></i></a>)</small>'
        else:
            return f'<a href="{maps_url}" target="_blank">{place_name} <i class="bi bi-geo-alt-fill"></i></a>'

    processed_text = pattern.sub(replace_with_link, text_segment)
    # CLEAN stray markdown bolds
    processed_text = processed_text.replace("**", "")
    return processed_text

# =============================================================
# MAIN VIEWS
# =============================================================

def plan_trip_view(request):
    trip_type = request.session.get('trip_type', 'recreational')
    itinerary_html = None
    pdf_download_url = None
    unsplash_client = UnsplashAPIClient(settings.UNSPLASH_ACCESS_KEY)

    if request.method == 'POST':
        trip_type = request.POST.get('trip_type', 'recreational')
        form = TripPlanningForm(request.POST)

        if form.is_valid():
            budget = form.cleaned_data['budget']
            starting_point = form.cleaned_data['starting_point']
            destination = form.cleaned_data['destination']
            trip_duration_days = form.cleaned_data['trip_duration_days']
            interests = [] if trip_type == 'devotional' else form.cleaned_data['interests']
            travel_mode_preference = form.cleaned_data['travel_mode_preference']
            accommodation_preference = form.cleaned_data['accommodation_preference']
            food_preference = form.cleaned_data['food_preference']

            try:
                gen_ai_client = MockGenAIClient() if settings.USE_MOCK_AI_CLIENT else GenAIClient(settings.GEN_AI_API_KEY)
                raw_ai_output = gen_ai_client.generate_itinerary(
                    budget=budget, starting_point=starting_point, destination=destination,
                    duration_days=trip_duration_days, interests=interests,
                    travel_mode_preference=travel_mode_preference,
                    accommodation_preference=accommodation_preference,
                    food_preference=food_preference,
                    trip_type=trip_type
                )
                if not raw_ai_output or "Could not generate itinerary" in raw_ai_output:
                    messages.error(request, "Failed to generate itinerary. Please try again.")
                    raw_ai_output = None
            except Exception as e:
                messages.error(request, f"AI generation failed: {e}")
                raw_ai_output = None

            if raw_ai_output:
                structured_itinerary = parse_ai_itinerary_to_structure(raw_ai_output)

                # Inject form data
                structured_itinerary.update({
                    'budget': float(budget),
                    'destination': destination,
                    'starting_point': starting_point,
                    'trip_duration_days': trip_duration_days,
                    'interests': interests,
                    'travel_mode_preference': travel_mode_preference,
                    'accommodation_preference': accommodation_preference,
                    'food_preference': food_preference
                })

                html_output = []
                dest_city_only = destination.split(',')[0].strip()

                # Notes
                for note in structured_itinerary.get("notes_before_days", []):
                    html_output.append(f'<p>{note}</p>')
                html_output.append("\n")

                # Days loop
                for day in structured_itinerary["days"]:
                    image_query = f"{day['theme']} {dest_city_only}"
                    image_url = unsplash_client.search_image(image_query)
                    if image_url:
                        html_output.append(f'<img src="{image_url}" class="itinerary-image img-fluid mb-3" alt="Image for {day["theme"]}">')
                    html_output.append(f'<h3 class="day-heading">Day {day["day_number"]}: {day["theme"]}</h3>')
                    html_output.append('<ul class="list-group list-group-flush mb-3">')

                    for section_name, content in day["sections"].items():
                        if section_name in ["Travel", "Accommodation"] and content:
                            linked = generate_place_links_html(content, dest_city_only)
                            html_output.append(f'<li class="list-group-item"><strong>{section_name}:</strong> {linked}</li>')
                        elif section_name in ["Food", "Activities"] and content:
                            html_output.append(f'<li class="list-group-item"><strong>{section_name}:</strong>')
                            html_output.append('<ul class="list-unstyled nested-list">')
                            for item in content:
                                details_raw = item.get("details", item)
                                linked_details = generate_place_links_html(details_raw, dest_city_only)
                                if section_name == "Food" and item.get("type") and item["type"] != "Generic":
                                    html_output.append(f"<li><strong>{item['type']}:</strong> {linked_details}</li>")
                                else:
                                    html_output.append(f"<li>{linked_details}</li>")
                            html_output.append('</ul></li>')

                    html_output.append('</ul>\n<hr>\n')

                # Budget summary
                budget_summary = structured_itinerary.get("budget_summary", {})
                if budget_summary.get("header"):
                    html_output.append(f'<h3>{budget_summary["header"].strip("*")}</h3>')
                    html_output.append('<ul class="list-group list-group-flush mb-3">')
                    for item in budget_summary.get("items", []):
                        html_output.append(f'<li class="list-group-item">{item.lstrip("*").lstrip("•").strip()}</li>')
                    if budget_summary.get("total"):
                        total_text = budget_summary["total"].strip("*").strip()
                        html_output.append(f'<li class="list-group-item total-line"><strong>{total_text}</strong></li>')
                    html_output.append('</ul>')

                    if budget_summary.get("tips"):
                        html_output.append('<h4>Tips for Budget Management:</h4>')
                        html_output.append('<ul class="list-group list-group-flush">')
                        for tip in budget_summary["tips"]:
                            html_output.append(f'<li class="list-group-item">{tip.lstrip("*").lstrip("•").strip()}</li>')
                        html_output.append('</ul>')

                itinerary_html = "\n".join(html_output)
                request.session['itinerary_data_for_pdf'] = structured_itinerary
                pdf_download_url = '/plan/download-itinerary-pdf/'

        else:
            messages.error(request, "Please correct the errors in your input.")
    else:
        form = TripPlanningForm(initial={'trip_type': trip_type})

    context = {
        'form': form,
        'itinerary_html': itinerary_html,
        'pdf_download_url': pdf_download_url,
        'trip_type': trip_type
    }
    return render(request, 'trip_planner_app/plan_trip.html', context)


def download_itinerary_pdf_view(request):
    structured_itinerary_data = request.session.get('itinerary_data_for_pdf')
    if not structured_itinerary_data:
        messages.error(request, "No itinerary data found to generate PDF.")
        return HttpResponse("No itinerary data found. Please generate a plan first.", status=404)

    try:
        pdf_buffer = generate_itinerary_pdf(structured_itinerary_data)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="personalized_trip_itinerary.pdf"'
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, f"Error generating PDF: {e}.")
        return HttpResponse(f"Error generating PDF. Please try again. ({e})", status=500)
