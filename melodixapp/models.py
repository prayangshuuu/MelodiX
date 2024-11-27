from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
import uuid


# ----------------------------
# User Model
# ----------------------------

class User(AbstractUser):
    """Custom User model."""
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='profile_pictures/default_user.png',
        blank=True,
        null=True
    )
    date_joined = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        """Ensure the username is saved in lowercase."""
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# ----------------------------
# Label Model
# ----------------------------

class Label(models.Model):
    """Model to manage labels."""
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# ----------------------------
# Artist Model
# ----------------------------

class Artist(models.Model):
    """Model to manage artists."""
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# ----------------------------
# Genre Model
# ----------------------------

class Genre(models.Model):
    """Model to manage genres."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ----------------------------
# Subgenre Model
# ----------------------------

class Subgenre(models.Model):
    """Model to manage subgenres."""
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, related_name='subgenres', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.genre.name})"


# ----------------------------
# Release Model
# ----------------------------

class Release(models.Model):
    """Model to manage music releases."""
    RELEASE_FORMATS = [
        ('SINGLE', 'Single'),
        ('EP', 'EP'),
        ('ALBUM', 'Album'),
    ]
    PRICE_TIERS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255, blank=True, null=True)
    primary_artists = models.ManyToManyField(Artist, related_name='primary_releases')
    featuring_artists = models.ManyToManyField(Artist, blank=True, related_name='featuring_releases')
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True)
    release_format = models.CharField(max_length=10, choices=RELEASE_FORMATS, default='SINGLE')
    upc_ean = models.CharField(max_length=12, blank=True, null=True)
    catalogue_number = models.CharField(max_length=50, blank=True, null=True)
    release_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Copyright and Production Info
    copyright_holder = models.CharField(max_length=255, default="Unknown")
    copyright_year = models.PositiveIntegerField(default=now().year)
    production_holder = models.CharField(max_length=255, default="Unknown")
    production_year = models.PositiveIntegerField(default=now().year)

    # Additional Info
    artwork = models.ImageField(upload_to='release_artworks/', null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    subgenre = models.ForeignKey(Subgenre, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=100, default="English")
    release_date = models.DateField(default=now)
    availability_date = models.DateField(default=now)
    price_tier = models.CharField(max_length=10, choices=PRICE_TIERS, default='MEDIUM')
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='releases')

    def __str__(self):
        return self.title


# ----------------------------
# Track Model
# ----------------------------

class Track(models.Model):
    """Model to manage individual tracks within releases."""
    TRACK_TYPES = [
        ('ORIGINAL', 'Original'),
        ('KARAOKE', 'Karaoke'),
        ('MEDLEY', 'Medley'),
        ('COVER', 'Cover'),
    ]
    PARENTAL_ADVISORY_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('CLEANED', 'Cleaned'),
    ]

    release = models.ForeignKey(Release, related_name='tracks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TRACK_TYPES, default='ORIGINAL')
    is_instrumental = models.BooleanField(default=False)
    file = models.FileField(upload_to='track_files/', null=True, blank=True)
    artist = models.ManyToManyField(Artist, related_name='track_artists')
    isrc = models.CharField(max_length=12, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    subgenre = models.ForeignKey(Subgenre, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=100, default="English")
    lyrics_language = models.CharField(max_length=100, blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)

    # Copyright Info
    production_year = models.PositiveIntegerField(default=now().year)
    copyright_holder = models.CharField(max_length=255, default="Unknown")
    copyright_year = models.PositiveIntegerField(default=now().year)
    sound_recording_copyright = models.CharField(max_length=255, blank=True, null=True)

    parental_advisory = models.CharField(max_length=10, choices=PARENTAL_ADVISORY_CHOICES, default='NO')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self):
        return f"{self.title} ({self.release.title})"


# ----------------------------
# Store Model
# ----------------------------

class Store(models.Model):
    """Model to manage digital stores for releases."""
    STORE_TYPES = [
        ('DOWNLOADS', 'Downloads'),
        ('STREAMING', 'Streaming'),
        ('BOTH', 'Both'),
    ]

    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='store_logos/')
    store_type = models.CharField(max_length=10, choices=STORE_TYPES, default='BOTH')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
