from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = PhoneNumberField(max_length = 15, default = '+91', blank = True, null = True)
    is_freelancer = models.BooleanField(default= False)
    is_client = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
