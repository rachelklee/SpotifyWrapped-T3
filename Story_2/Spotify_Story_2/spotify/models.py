from django.db import models
from django.contrib.auth.models import User

class SpotifyAccount(models.Model):
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
