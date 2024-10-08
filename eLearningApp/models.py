from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
timezone.now
# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} about {self.subject}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

# class Course(models.Model):
#     CATEGORY_CHOICES = [
#         ('programming', 'Programming'),
#         ('design', 'Design'),
#         ('business', 'Business'),
#         ('marketing', 'Marketing'),
#         ('other', 'Other'),
#     ]

#     title = models.CharField(max_length=200)
#     description = models.TextField(default="No description available")
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
#     course_image = models.ImageField(upload_to='course_images/', null=True, blank=True)
#     course_file = models.FileField(upload_to='course_files/', null=True, blank=True)
#     # instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
#     instructor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
#     # instructor = models.ForeignKey(User, on_delete=models.CASCADE, default=some_existing_user_id)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is updated
    
#     def __str__(self):
#         return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    content_upload = models.FileField(upload_to='course_content/', blank=True, null=True)

    def __str__(self):
        return self.title
    


