from django.db import models
from django.contrib.auth.models import User
from gallery.models.album import Album
from gallery.models.photo import Photo

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_albums = models.ManyToManyField(Album, blank=True, related_name='favorited_by')
    favorite_photos = models.ManyToManyField(Photo, blank=True, related_name='favorited_by')

    def __str__(self):
        return self.user.username
