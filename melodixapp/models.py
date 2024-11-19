from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    """Custom user model that extends AbstractUser."""
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='profile_pictures/default_user.png',
        blank=True,
        null=True
    )
    date_joined = models.DateTimeField(default=now)  # Override default to ensure consistency

    def save(self, *args, **kwargs):
        # Ensure username is always lowercase
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
