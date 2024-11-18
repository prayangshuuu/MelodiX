from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model that extends AbstractUser."""
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
