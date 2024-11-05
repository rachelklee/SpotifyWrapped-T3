from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from spotify.models import SpotifyAccount
import json

# Create your views here.
def register_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please try another one."
        else:
            # Create a new user
            User.objects.create_user(username=username, password=password)
            return redirect('api:login_user')
    
    return render(request, 'api/register.html', {'error_message': error_message})

def login_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to a success page
            login(request, user)
            #return HttpResponse("Login successful.")
            return redirect('spotify:spotify_login')
        else:
            # If authentication fails, send an error message
            error_message = "Invalid username or password."
    
    return render(request, 'api/login.html', {'error_message':error_message})

def logout_user(request):
    logout(request)
    return render(request, 'api/logout.html')
    #return redirect('api:login_user')  # Redirect to the login page after logout

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
        except SpotifyAccount.DoesNotExist:
            spotify_wraps = None  # Handle case where there is no Spotify account
    else:
        spotify_wraps = None  # Handle case where user is not logged in

    wraps_list=[]
    if (spotify_wraps != None):
        for item in spotify_wraps.get('items'):
            album = item.get('album').get('name')
            artist = item.get('album').get('artists')[0].get('name')
            print(album + " : " + artist)
            wraps_list.append(album + " : " + artist)
    return render(request, 'api/display_user.html', {'user': user, 'wraps_list': wraps_list})

def main(request):
    return create_user(request)
    #return HttpResponse("Hello")

