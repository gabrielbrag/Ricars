from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    document = models.CharField(max_length=14)
    name = models.CharField(max_length=50, default='')