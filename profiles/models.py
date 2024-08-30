from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username
