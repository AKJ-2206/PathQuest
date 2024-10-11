from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
timezone.now

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
    

class Course(models.Model):
    title = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    content_upload = models.FileField(upload_to='course_content/', blank=True, null=True)
    course_files = models.FileField(upload_to='course_files/', null=True, blank=True)

    likers = models.ManyToManyField(User, related_name='liked_courses', blank=True)
    cart_users = models.ManyToManyField(User, related_name='cart_courses', blank=True)
    buyers = models.ManyToManyField(User, related_name='bought_courses', blank=True)

    def __str__(self):
        return self.title
    
class File(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_files/')



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.course.title}"
    

