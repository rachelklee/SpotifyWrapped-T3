from django.urls import path
from . import views

app_name = 'spotify'

urlpatterns = [
    path('login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('generate/', views.generate_wrap, name='generate_wrap'),
]
