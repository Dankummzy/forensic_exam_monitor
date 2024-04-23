from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    LEVEL_CHOICES = [
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
        (500, '500 Level'),
        (600, '600 Level'),
    ]

    FACULTY_CHOICES = [
        ('Faculty of Arts', 'Faculty of Arts'),
        ('Faculty of Science', 'Faculty of Science'),
        ('Faculty of Engineering', 'Faculty of Engineering'),
        # Add other faculty choices as needed
    ]

    DEPARTMENT_CHOICES = [
        ('Department of History', 'Department of History'),
        ('Department of Biology', 'Department of Biology'),
        ('Department of Computer Science', 'Department of Computer Science'),
        # Add other department choices as needed
    ]

    matriculation_number = models.CharField(max_length=20, blank=True)
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES, blank=True, null=True)
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES, blank=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
