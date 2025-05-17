from django.db import models
from accounts.models import User

# Create your models here.

class Job(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    title = models.CharField(max_length=255)
    salary = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    experience = models.PositiveIntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return self.title
