# router/urls.py

from django.urls import path
from . import views

app_name = 'router'

urlpatterns = [
    # FIX: Only define the path for the choice page and its POST submission.
    path('select/', views.trip_choice, name='trip_choice'), 
    # NOTE: The name 'trip_choice' remains the primary reference.
]