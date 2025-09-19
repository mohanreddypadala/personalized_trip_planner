# core/views.py
from django.shortcuts import render

def index(request):
    """Home page view."""
    return render(request, 'core/index.html')

def about(request):
    """About project and moto page view."""
    return render(request, 'core/about.html')

def team(request):
    """Team information page view."""
    return render(request, 'core/team.html')