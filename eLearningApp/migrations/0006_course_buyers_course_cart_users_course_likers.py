# Generated by Django 5.1.1 on 2024-10-10 17:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLearningApp', '0005_course_course_files'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='buyers',
            field=models.ManyToManyField(blank=True, related_name='bought_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='cart_users',
            field=models.ManyToManyField(blank=True, related_name='cart_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
