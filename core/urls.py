# core/urls.py
from django.urls import path
from . import views

app_name = 'core' # Namespace for URLs

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
]