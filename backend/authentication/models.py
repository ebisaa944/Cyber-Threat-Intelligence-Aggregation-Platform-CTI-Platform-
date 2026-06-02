from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('analyst', 'SOC Analyst'),
        ('researcher', 'Threat Researcher'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='analyst')

    def __str__(self):
        return f"{self.username} ({self.role})"