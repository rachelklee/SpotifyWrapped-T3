from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'spotify'

urlpatterns = [
    path('login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('generate/', views.generate_wrap, name='generate_wrap'),
]
