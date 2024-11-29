
from django.db import models
from django.contrib.auth.models import User


"""
Spotify Account and Wrap Models
===============================

This module defines Django models for managing Spotify account data and storing personalized
Spotify Wrap data for users, including seasonal variations like Halloween and Christmas wraps.

Models
------
1. SpotifyAccount:
    - Represents a user's Spotify account details, including tokens for authentication
      and seasonal wrap data.

2. SpotifyWrap:
    - Stores general Spotify wrap data for a user.

3. HalloweenWrap:
    - Stores Halloween-themed Spotify wrap data for a user.

4. ChristmasWrap:
    - Stores Christmas-themed Spotify wrap data for a user.

Classes
-------
"""

class SpotifyAccount(models.Model):
    """
    A model representing a user's Spotify account.

    Attributes:
        user (OneToOneField): Links the Spotify account to a specific user. Deleting
            the user also deletes the Spotify account.
        spotify_id (CharField): Stores the user's Spotify account ID (max length 50).
        access_token (CharField): Stores the access token for Spotify API (max length 255).
        refresh_token (CharField): Stores the refresh token for Spotify API (max length 255).
        token_expires (DateTimeField): Specifies when the access token expires.
        wraps (JSONField): Stores general wrap data in JSON format.
        halloweenwrap (JSONField): Stores Halloween wrap data in JSON format.
        christmaswrap (JSONField): Stores Christmas wrap data in JSON format.
        client_id (CharField): Stores the Spotify API client ID (default="").
        client_secret (CharField): Stores the Spotify API client secret (default="").

    Methods:
        __str__(): Returns a string representation of the Spotify account linked to the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expires = models.DateTimeField()
    wraps = models.JSONField(default=dict, blank=True)
    halloweenwrap = models.JSONField(default=dict, blank=True)
    christmaswrap = models.JSONField(default=dict, blank=True)
    client_id = models.CharField(max_length=255,default="")
    client_secret = models.CharField(max_length=255,default="")

    def __str__(self):
        return f"{self.user.username}'s Spotify Account"

class SpotifyWrap(models.Model):
    """
    A model to store general Spotify wrap data for a user.

    Attributes:
        user (ForeignKey): Links the wrap data to a specific user. Deletes wrap data
            if the user is deleted.
        wrap_data (JSONField): Stores the wrap data in JSON format.
        date_created (DateTimeField): Automatically records the creation date and time.

    Methods:
        __str__(): Returns a string representation of the Spotify wrap data linked to the user.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wrap_data = models.JSONField()  # Stores wrap data as JSON
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Spotify Wrap {self.date_created}"



class HalloweenWrap(models.Model):
    """
       A model to store personalized Halloween-themed Spotify wrap data for a user.

       Attributes:
           user (ForeignKey): A reference to the `User` model, linking the Halloween
               wrap data to a specific user. Deletes the wrap data if the user is deleted.
           halloween_wrap_data (JSONField): A field to store the wrap data in JSON format,
               containing Spotify-generated Halloween-themed track recommendations or statistics.
           date_created (DateTimeField): Automatically records the date and time when
               the Halloween wrap data was created.

       Usage:
           This model is used to store and retrieve Halloween-themed Spotify wrap data
           for individual users, allowing for customized seasonal music experiences.
       """
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    halloween_wrap_data = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s Halloween Wrap {self.date_created}"


class ChristmasWrap(models.Model):
    """
     A model to store personalized Christmas-themed Spotify wrap data for a user.

     Attributes:
         user (ForeignKey): A reference to the `User` model, linking the Christmas
             wrap data to a specific user. Deletes the wrap data if the user is deleted.
         christmas_wrap_data (JSONField): A field to store the wrap data in JSON format,
             containing Spotify-generated Christmas-themed track recommendations or statistics.
         date_created (DateTimeField): Automatically records the date and time when
             the Christmas wrap data was created.

     Usage:
         This model is used to store and retrieve Christmas-themed Spotify wrap data
         for individual users, enabling customized seasonal music experiences.
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    christmas_wrap_data = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Halloween Wrap {self.date_created}"
