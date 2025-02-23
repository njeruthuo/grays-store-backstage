from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=14, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
