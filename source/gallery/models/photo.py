from django.db import models
from django.contrib.auth.models import User
import uuid
from gallery.models.album import Album


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', blank=False, null=False, verbose_name='Image')
    caption = models.TextField(max_length=255, blank=False, null=False, verbose_name='Caption')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', verbose_name='Author')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos', verbose_name='Album')
    is_private = models.BooleanField(default=False, verbose_name='Is private')
    token = models.CharField(max_length=36, unique=True, null=True, blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def generate_token(self):
        if not self.token:
            self.token = str(uuid.uuid4())
            self.save()