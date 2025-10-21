# personalized_trip_planner/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. CORE APP: Handles the actual Home page (/) and About/Team
    # NOTE: This MUST be path('') to catch the root URL
    path('', include('core.urls')), 
    
    # 2. ROUTER APP: Handles the trip-type selection page.
    path('choice/', include('router.urls')), 

    # 3. TRIP PLANNER APP
    path('plan/', include('trip_planner_app.urls')),
]