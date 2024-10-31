from django.contrib import admin
from .models import User, Genre, AnimeType, Anime, Review


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active")


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("title", "anime_type", "status", "start_date", "end_date")
    list_filter = ("anime_type", "status")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "character", "rating")


admin.site.register(Genre)
admin.site.register(AnimeType)
