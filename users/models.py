from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='users'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
