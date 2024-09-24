from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from django.contrib import admin
from .models import ContactMessage, Profile

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('sent_at',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'profile_photo_display')
    
    def profile_photo_display(self, obj):
        if obj.profile_photo:
            return '<img src="%s" width="100" height="100" />' % obj.profile_photo.url
        return 'No Image'
    profile_photo_display.allow_tags = True
    profile_photo_display.short_description = 'Profile Photo'

admin.site.register(Profile, ProfileAdmin)


class UserAdmin(BaseUserAdmin):
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

users = User.objects.all()
for user in users:
    Profile.objects.get_or_create(user=user)
