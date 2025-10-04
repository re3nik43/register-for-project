from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser
    Stores additional information from OAuth providers
    """
    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)  # google, github, facebook, apple
    provider_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
