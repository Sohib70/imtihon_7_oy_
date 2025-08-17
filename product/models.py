from django.db import models

from users.models import CustomUser


# Create your models here.

class Category(models.Model):
    nomi = models.CharField(max_length=100)

    def __str__(self):
        return self.nomi


class Avtotovarlar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(max_length=100)
    firmasi = models.CharField(max_length=100)
    tavsifi = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name