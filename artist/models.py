from django.db import models
from django.conf import settings


class Artist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artist_profile')
    bio = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    genres = models.JSONField(default=list)  # Storing as array of strings
    social_media = models.JSONField(default=dict)  # {'instagram': '', 'twitter': ''}
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(blank=True)
    portfolio_links = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
