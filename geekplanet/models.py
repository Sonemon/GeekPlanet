from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

import uuid


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self) -> str:
        return self.username

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return settings.DEFAULT_PROFILE_PICTURE_URL


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class AnimeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    anime_type_description = models.TextField()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Anime(models.Model):
    STATUS_CHOICES = [
        ("released", "Released"),
        ("ongoing", "Ongoing"),
        ("announcement", "Announcement"),
        ("cancelled", "Cancelled"),
    ]
    DEFAULT_ANIME_PICTURE_URL = "/media/anime_pictures/default.png"

    title = models.CharField(max_length=200)
    anime_picture = models.ImageField(upload_to="anime_pictures/", null=True, blank=True)
    alternate_titles = models.TextField(blank=True)
    anime_type = models.ForeignKey(AnimeType, on_delete=models.CASCADE, related_name="animes")
    episodes = models.PositiveIntegerField()
    episode_duration = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name="animes")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    user_rating = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_anime_picture(self):
        if self.anime_picture:
            return self.anime_picture.url
        else:
            return self.DEFAULT_ANIME_PICTURE_URL

    import uuid

    def save(self, *args, **kwargs):
        if self.anime_picture:
            # unique name for anime_pictures
            self.anime_picture.name = f"{uuid.uuid4()}_picture.png"

        super().save(*args, **kwargs)


class Review(models.Model):
    CHARACTER_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField()
    character = models.CharField(max_length=10, choices=CHARACTER_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.related_object}"
