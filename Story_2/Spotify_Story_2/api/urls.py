from django.urls import path
from .views import main, login_user, logout_user, delete_user, display_user
from . import views

app_name = 'api'

urlpatterns = [
    path('home', main),
    path('', main),
    path('register/', views.register_user, name='register_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.display_user, name='display_user'),
    path('get_halloween_wrap/', views.get_halloween_wrap, name='get_halloween_wrap'),
    path('get_christmas_wrap/', views.get_christmas_wrap, name = 'get_christmas_wrap'),
    path('delete_wraps/', views.delete_wraps, name='delete_wraps'),
    path('contact/', views.contact, name='contact'),
    path('top_songs/', views.top_songs, name='top_songs'),
    path('top_artists/', views.top_artists, name='top_artists'),
    path('top_artist_single/', views.top_artist_single, name='top_artist_single'),
    path('top_artist_transition/', views.top_artist_transition, name='top_artist_transition'),
    path('number_of_artists/', views.number_of_artists, name='number_of_artists'),
    path('end/', views.end, name='end'),
    path('music_guessing_game/', views.music_guessing_game, name='music_guessing_game'),

]
