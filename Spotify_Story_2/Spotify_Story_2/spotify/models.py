from django.db import models
from django.contrib.auth.models import User

class SpotifyAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expires = models.DateTimeField()
    wraps = models.JSONField(default=dict, blank=True)
    halloweenwrap = models.JSONField(default = dict, blank = True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hwrap_data = models.JSONField()  # Stores wrap data as JSON
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Halloween Wrap {self.date_created}"
