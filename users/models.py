from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    adres = models.CharField(max_length=120, blank=True , null=True)

    def __str__(self):
        return self.username