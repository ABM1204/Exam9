from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    is_private = models.BooleanField(default=False, verbose_name='Is private')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


