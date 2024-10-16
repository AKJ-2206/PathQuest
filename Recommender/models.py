# recommender/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

# recommender/admin.py
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)