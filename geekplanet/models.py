from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class User(AbstractUser):
    profile_picture = CloudinaryField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self) -> str:
        return self.username


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

    title = models.CharField(max_length=200)
    anime_picture = CloudinaryField(null=True, blank=True)
    alternate_titles = models.TextField(blank=True)
    anime_type = models.ForeignKey(AnimeType, on_delete=models.CASCADE, related_name="animes")
    episodes = models.PositiveIntegerField()
    episode_duration = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name="animes")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @property
    def average_rating(self) -> float:
        anime_content_type = ContentType.objects.get_for_model(Anime)

        average = Review.objects.filter(
            content_type=anime_content_type,
            object_id=self.id
        ).aggregate(models.Avg('rating'))['rating__avg']

        return round(average, 2) if average is not None else 0.0

    def get_reviews(self):
        return Review.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        )

    def rew_count(self):
        return Review.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()


class Review(models.Model):
    CHARACTER_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    character = models.CharField(max_length=10, choices=CHARACTER_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.related_object}"

    def clean(self, user=None):
        if user is not None and Review.objects.filter(
            user=user,
            content_type=self.content_type,
            object_id=self.object_id,
        ).exists():
            raise ValidationError("You have already reviewed this content.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
