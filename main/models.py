from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    category = models.CharField(max_length=100)


class Order(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
