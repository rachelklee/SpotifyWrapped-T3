from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from spotify.models import SpotifyAccount
import json
from django.utils import timezone
import datetime
from datetime import timedelta


# Create your views here.
def register_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please try another one."
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            spotify_account, created = SpotifyAccount.objects.get_or_create(
                user=user,
                client_id=client_id,
                client_secret=client_secret,
                defaults={
                    'token_expires': timezone.now() + timedelta(days=32)
                }
            )

            return redirect('api:login_user')

    return render(request, 'api/register.html', {'error_message': error_message})


def login_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to a success page
            login(request, user)
            return redirect('spotify:spotify_login')
        else:
            # If authentication fails, send an error message
            error_message = "Invalid username or password."

    return render(request, 'api/login.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return render(request, 'api/logout.html')
    # return redirect('api:login_user')  # Redirect to the login page after logout


def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if the user exists and delete them
        try:
            user = User.objects.get(username=username)
            user.delete()
            return redirect('api:login_user')
        except User.DoesNotExist:
            return HttpResponse(f"User '{username}' does not exist.")

    # Retrieve all users to display in the dropdown
    users = User.objects.all()
    return render(request, 'api/delete_user.html', {'users': users})


def delete_wraps(request):
    if request.method == 'POST':
        user = request.user
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            spotify_account.wraps = None
            spotify_account.halloweenwrap = None
            spotify_account.christmaswrap = None
            wraps_list = []
        except SpotifyAccount.DoesNotExist:
            wraps_list = []
    return render(request, 'api/display_user.html', {'user': user, 'wraps_list': wraps_list})


@login_required
def display_user(request):
    user = request.user
    if request.user.is_authenticated:  # Ensure the user is logged in
        user = request.user
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            spotify_wraps = spotify_account.wraps
            #halloween = spotify_account.halloweenwrap
        except SpotifyAccount.DoesNotExist:
            spotify_wraps = None  # Handle case where there is no Spotify account
    else:
        spotify_wraps = None  # Handle case where user is not logged in

    wraps_list = []
    if (spotify_wraps != None):
        for item in spotify_wraps.get('items')[:10]:
            album = item.get('album').get('name')
            image = item.get('album').get('images')[0].get('url')
            artist = item.get('album').get('artists')[0].get('name')
            preview_url = item.get('preview_url')  # Get the 30-second preview URL
            print(album + " : " + artist)
            wraps_list.append({
                'album': album,
                'artist': artist,
                'image': image,
                'preview_url': preview_url  # Include the preview URL
            })

    # wraps_song_list = []
    # if (spotify_wraps != None):
    #     for item in spotify_wraps.get('items')[:5]:
    #         album = item.get('album').get('name')
    #         image = item.get('album').get('images')[0].get('url')
    #         artist = item.get('album').get('artists')[0].get('name')
    #         preview_url = item.get('preview_url')  # Get the 30-second preview URL
    #         print(album + " : " + artist)
    #         wraps_song_list.append({
    #         'album': album,
    #         'artist': artist,
    #         'image': image,
    #         'preview_url': preview_url  # Include the preview URL
    #     })
            # print(album + " : " + artist)
            # wraps_list.append(album + " : " + artist)
        # if halloween and 'tracks' in halloween:
        #
        #     for i, track in enumerate(halloween['tracks']):
        #         track_name = track['name']
        #         artist_name = track['artists'][0]['name']
        #         link = track['artists'][0]['external_urls']['spotify']
        #         print(track_name + " : " + artist_name)
        #         wraps_list.append(track_name + " : " + artist_name + " : " + link)

    return render(request, 'api/display_user.html', {'user': user, 'wraps_list': wraps_list})



@login_required
def get_halloween_wrap(request):
    """
       Retrieve and display the user's Halloween-themed Spotify wrap data.

       This view fetches the user's stored Halloween wrap data from their linked Spotify account
       and prepares it for display. It handles cases where the user is not authenticated or does
       not have a linked Spotify account.

       Args:
           request (HttpRequest): The HTTP request object containing the current user.

       Returns:
           HttpResponse: Renders the `display_halloween.html` template with the Halloween wrap data.

       Raises:
           SpotifyAccount.DoesNotExist: If no Spotify account is linked to the user, an empty
           Halloween wrap will be displayed.

       """


    user = request.user
    halloween_list = []

    if request.user.is_authenticated:  # Ensure the user is logged in
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            halloween = spotify_account.halloweenwrap
        except SpotifyAccount.DoesNotExist:
            halloween = None  # Handle case where there is no Spotify account
    else:
        halloween = None  # Handle case where user is not logged in
    if halloween and 'tracks' in halloween:

         for i, track in enumerate(halloween['tracks']):
             track_name = track['name']
             artist_name = track['artists'][0]['name']
             link = track['artists'][0]['external_urls']['spotify']
             image_url = track['album']['images'][0]['url']
             print(track_name + " : " + artist_name)
             halloween_list.append({
                 'track_name': track_name,
                 'artist_name': artist_name,
                 'link': link,
                 'image_url': image_url,  # Include the image URL
             })
    return render(request, 'api/display_halloween.html', {'user': user, 'halloween_list': halloween_list})




@login_required
def get_christmas_wrap(request):
    """
       Retrieve and display the user's Christmas-themed Spotify wrap data.

       This view fetches the user's stored Christmas wrap data from their linked Spotify account
       and prepares it for display. If the user is not authenticated or does not have a linked
       Spotify account, the function handles these cases gracefully.

       Args:
           request (HttpRequest): The HTTP request object containing the current user.

       Returns:
           HttpResponse: Renders the `display_christmas.html` template with the Christmas wrap data.

       Raises:
           SpotifyAccount.DoesNotExist: If no Spotify account is linked to the user, an empty
           Christmas wrap will be displayed.

       """
    user = request.user
    christmas_list = []

    if request.user.is_authenticated:  # Ensure the user is logged in
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            christmas = spotify_account.christmaswrap
        except SpotifyAccount.DoesNotExist:
            christmas = None  # Handle case where there is no Spotify account
    else:
        christmas = None  # Handle case where user is not logged in
    if christmas and 'tracks' in christmas:

         for i, track in enumerate(christmas['tracks']):
             track_name = track['name']
             artist_name = track['artists'][0]['name']
             link = track['artists'][0]['external_urls']['spotify']
             image_url = track['album']['images'][0]['url']  # Get the album image URL
             print(track_name + " : " + artist_name)
             christmas_list.append({
                 'track_name': track_name,
                 'artist_name': artist_name,
                 'link': link,
                 'image_url': image_url,  # Include the image URL
             })
    return render(request, 'api/display_christmas.html', {'user': user, 'christmas_list': christmas_list})


def contact(request):
    return render(request, 'api/contact.html')

@login_required
def top_songs(request):
    user = request.user
    wraps_list = []

    if request.user.is_authenticated:  # Ensure the user is logged in
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            spotify_wraps = spotify_account.wraps  # Get the wraps data
        except SpotifyAccount.DoesNotExist:
            spotify_wraps = None  # Handle case where there is no Spotify account

    if spotify_wraps:
        for item in spotify_wraps.get('items')[:10]:  # Adjust the number of items as needed
            album = item.get('album').get('name')
            image = item.get('album').get('images')[0].get('url')
            artist = item.get('album').get('artists')[0].get('name')
            preview_url = item.get('preview_url')  # Get the preview URL
            wraps_list.append({
                'album': album,
                'artist': artist,
                'image': image,
                'preview_url': preview_url  # Include the preview URL
            })

    return render(request, 'api/top_songs.html', {'wraps_list': wraps_list})

@login_required
def top_artists(request):
    user = request.user
    if request.user.is_authenticated:  # Ensure the user is logged in
        user = request.user
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            spotify_wraps = spotify_account.wraps
            #halloween = spotify_account.halloweenwrap
        except SpotifyAccount.DoesNotExist:
            spotify_wraps = None  # Handle case where there is no Spotify account
    else:
        spotify_wraps = None  # Handle case where user is not logged in
    wraps_list = []
    if (spotify_wraps != None):
        for item in spotify_wraps.get('items')[:10]:
            album = item.get('album').get('name')
            image = item.get('album').get('images')[0].get('url')
            artist = item.get('album').get('artists')[0].get('name')
            preview_url = item.get('preview_url')  # Get the 30-second preview URL
            print(album + " : " + artist)
            wraps_list.append({
                'album': album,
                'artist': artist,
                'image': image,
                'preview_url': preview_url  # Include the preview URL
            })
    return render(request, 'api/top_artists.html', {'wraps_list': wraps_list})

@login_required
def top_artist_single(request):
    user = request.user
    if request.user.is_authenticated:  # Ensure the user is logged in
        user = request.user
        try:
            spotify_account = SpotifyAccount.objects.get(user=user)
            spotify_wraps = spotify_account.wraps
            #halloween = spotify_account.halloweenwrap
        except SpotifyAccount.DoesNotExist:
            spotify_wraps = None  # Handle case where there is no Spotify account
    else:
        spotify_wraps = None  # Handle case where user is not logged in
    single_wraps_list = []
    if (spotify_wraps != None):
        for item in spotify_wraps.get('items')[:10]:
            album = item.get('album').get('name')
            image = item.get('album').get('images')[0].get('url')
            artist = item.get('album').get('artists')[0].get('name')
            preview_url = item.get('preview_url')  # Get the 30-second preview URL
            print(album + " : " + artist)
            single_wraps_list.append({
                'album': album,
                'artist': artist,
                'image': image,
                'preview_url': preview_url  # Include the preview URL
            })
        return render(request, 'api/top_artist_single.html', {'single_wraps_list': single_wraps_list[0] if single_wraps_list else None})



def main(request):
    return create_user(request)
    # return HttpResponse("Hello")

