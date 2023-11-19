from django.contrib import admin
from .models import User, UserProfile

# Register the User model
admin.site.register(User)

# Register the UserProfile model
admin.site.register(UserProfile)
