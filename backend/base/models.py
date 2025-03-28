from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to use the custom user model

class Profile(models.Model):
    # Reference the custom user model here
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.user.username

    
class Product(models.Model):
    _id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)  # Store relative image path
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title