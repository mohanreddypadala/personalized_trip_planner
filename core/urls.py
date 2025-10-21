# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # FIX: Path for the core home page is now the empty string ''. 
    # This makes 'core:home' match the project root '/'.
    path('', views.index, name='home'), 
    
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
]