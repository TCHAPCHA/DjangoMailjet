from django.db import models
from django.utils import timezone


class Codes(models.Model):
    unique_id = models.CharField(max_length=255)
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)