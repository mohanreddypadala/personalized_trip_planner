# trip_planner_app/urls.py
from django.urls import path
from . import views

app_name = 'trip_planner_app' # Namespace for URLs

urlpatterns = [
    # This view will be accessible at /plan/ due to project-level routing
    path('', views.plan_trip_view, name='plan_trip'),
    # This view will be accessible at /plan/download-itinerary-pdf/
    path('download-itinerary-pdf/', views.download_itinerary_pdf_view, name='download_itinerary_pdf'),
]