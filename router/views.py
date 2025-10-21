# router/views.py

from django.shortcuts import render, redirect
from django.urls import reverse

# NOTE: The 'home_redirect' function is intentionally removed/not needed.

def trip_choice(request):
    """Handles the user selection of trip type (Devotional/Recreational)."""
    if request.method == 'POST':
        trip_type = request.POST.get('trip_type')
        
        if trip_type in ['devotional', 'recreational']:
            # Store the user's choice in the session before redirecting to the form
            request.session['trip_type'] = trip_type
            # Redirect to the main planning form
            return redirect(reverse('trip_planner_app:plan_trip'))
        else:
            return render(request, 'router/trip_type_choice.html', {'error': 'Please select a valid trip type.'})

    # When accessing via GET
    current_trip_type = request.session.get('trip_type', 'recreational')
    return render(request, 'router/trip_type_choice.html', {'current_trip_type': current_trip_type})