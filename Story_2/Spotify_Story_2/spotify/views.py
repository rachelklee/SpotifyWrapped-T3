from django.shortcuts import render, redirect
from Spotify_Story_2.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
from .models import SpotifyAccount, SpotifyWrap, HalloweenWrap, ChristmasWrap
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import requests
import datetime
from datetime import timedelta
import json

def spotify_login(request):
    """
       Redirect the user to Spotify's authorization page.

       This function initiates the authorization process by redirecting the user to the
       Spotify login page, allowing the application to gain access to the user's Spotify data.

       Args:
           request (HttpRequest): The HTTP request object.

       Returns:
           HttpResponseRedirect: Redirects the user to Spotify's authorization URL.
       """
    # Redirect user to Spotify's authorization page
    spotify_account = SpotifyAccount.objects.get(user=request.user)
    REDIRECT_URI="http://127.0.0.1:8000/spotify/callback"
    auth_url = (
        'https://accounts.spotify.com/authorize'
        f"?client_id={spotify_account.client_id}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=user-top-read"
    )
    return redirect(auth_url)

def spotify_callback(request):
    """
       Handle Spotify's callback after user authorization.

       This function retrieves the authorization code from Spotify and exchanges it
       for an access token and refresh token, which are then saved in the SpotifyAccount model.

       Args:
           request (HttpRequest): The HTTP request object containing the authorization code.

       Returns:
           HttpResponseRedirect: Redirects the user to the wrap generation page.
       """
    # Get the authorization code from Spotify
    spotify_account = SpotifyAccount.objects.get(user=request.user)
    code = request.GET.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://127.0.0.1:8000/spotify/callback",
        'client_id': spotify_account.client_id,
        'client_secret': spotify_account.client_secret,
    })
    response_data = response.json()
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    expires_in = response_data['expires_in']

    spotify_account.access_token = access_token
    spotify_account.refresh_token = refresh_token
    spotify_account.token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)
    spotify_account.save()

    return redirect('spotify:generate_wrap')

@login_required
def generate_wrap(request):
    """
        Generate a Spotify music wrap for the user.

        This function fetches the user's top Spotify tracks and stores the wrap data
        in the SpotifyWrap model for future retrieval.

        Args:
            request (HttpRequest): The HTTP request object containing the current user.

        Returns:
            HttpResponseRedirect: Redirects the user to the page that displays the wrap data.
        """
    # Fetch and display Spotify data
    user = request.user
    spotify_account = SpotifyAccount.objects.get(user=user)
    if spotify_account.token_expires < timezone.now():
        refresh_token(spotify_account)  # Refresh the token if it's expired

    headers = {
        "Authorization": f"Bearer {spotify_account.access_token}"
    }
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks'
    response = requests.get(top_tracks_url, headers=headers)
    wrap_data = response.json()
    spotify_account.wraps = wrap_data;
    spotify_account.save()

    # Save wrap data
    SpotifyWrap.objects.create(user=user, wrap_data=wrap_data)
    #return render(request, 'spotify/wrap_summary.html', {'wrap_data': wrap_data})
    #return render(request, 'api/display_user.html', {'wrap_data': wrap_data})
    return redirect('api:display_user')

def refresh_token(spotify_account):
    # Refresh Spotify access token
    """
        Refresh the Spotify access token.

        This function refreshes the user's Spotify access token when it has expired,
        allowing continued access to Spotify data.

        Args:
            spotify_account (SpotifyAccount): The user's Spotify account model instance.

        Returns:
            None
        """
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'refresh_token',
        'refresh_token': spotify_account.refresh_token,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })
    response_data = response.json()
    spotify_account.access_token = response_data['access_token']
    spotify_account.token_expires = timezone.now() + datetime.timedelta(seconds=response_data['expires_in'])
    spotify_account.save()

def generate_halloween_wrap(request):
    """
       Generate a personalized Halloween music wrap for the user.

       This function retrieves Halloween-themed track recommendations from Spotify's API
       using the user's linked Spotify account. It updates the stored data and creates
       a new `HalloweenWrap` database entry for future retrieval.

       Args:
           request (HttpRequest): The HTTP request object containing the current user.

       Returns:
           HttpResponseRedirect: Redirects the user to the 'api:get_halloween_wrap' URL.

       Raises:
           SpotifyAccount.DoesNotExist: If no Spotify account is linked to the user.
           requests.exceptions.RequestException: If the Spotify API request fails.
       """

    user = request.user
    spotify_account = SpotifyAccount.objects.get(user=user)
    spotify_account.refresh_from_db()
    if spotify_account.token_expires < timezone.now():
        refresh_token(spotify_account)


    headers = {
        "Authorization": f"Bearer {spotify_account.access_token}"
     }
    top_tracks_url = 'https://api.spotify.com/v1/recommendations?limit=10&seed_tracks=23V08GxMeaZNSf8Gy6KF6t%2C1dC459M55edeKPG6d1f1GX%2C1arUbkguEp9QR7e1Z4CAtd'
    response = requests.get(top_tracks_url,headers = headers)
    wrap_data = response.json()
    spotify_account.halloweenwrap = wrap_data
    spotify_account.save()

    HalloweenWrap.objects.create(user = user, halloween_wrap_data= wrap_data)

    return redirect('api:get_halloween_wrap')





def generate_christmas_wrap(request):
    """
        Generate a personalized Christmas music wrap for the user.

        This function fetches holiday-themed track recommendations from Spotify's API
        using the user's linked Spotify account, updates the account's stored data,
        and saves the results to the database for future retrieval.

        Args:
            request (HttpRequest): The HTTP request object containing the current user.

        Returns:
            HttpResponseRedirect: Redirects the user to the 'api:get_christmas_wrap' URL.

        Raises:
            SpotifyAccount.DoesNotExist: If no Spotify account is linked to the user.
            requests.exceptions.RequestException: If the Spotify API request fails.
        """
    user = request.user
    spotify_account = SpotifyAccount.objects.get(user=user)
    spotify_account.refresh_from_db()
    if spotify_account.token_expires < timezone.now():
        refresh_token(spotify_account)


    headers = {
        "Authorization": f"Bearer {spotify_account.access_token}"
     }
    top_tracks_url = 'https://api.spotify.com/v1/recommendations?limit=10&seed_genres=holiday&seed_tracks=0bYg9bo50gSsH3LtXe2SQn%2C6tjituizSxwSmBB5vtgHZE%2C2FRnf9qhLbvw8fu4IBXx78%2C7vQbuQcyTflfCIOu3Uzzya'
    response = requests.get(top_tracks_url,headers = headers)
    wrap_data = response.json()
    spotify_account.christmaswrap = wrap_data
    spotify_account.save()

    ChristmasWrap.objects.create(user = user, christmas_wrap_data= wrap_data)

    return redirect('api:get_christmas_wrap')










