from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    company = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
