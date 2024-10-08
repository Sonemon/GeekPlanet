from django.urls import path
from .views import (
    MainPageView,
    UserListView,
    UserDetailView,
    AnimeListView,
    AnimeCreateView,
    AnimeDetailView,
    AnimeUpdateView,
)

app_name = "geekplanet"

urlpatterns = [
    path("", MainPageView.as_view(), name="mainpage"),
    path("geeks/", UserListView.as_view(), name="user_list"),
    path("geeks/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("animes/", AnimeListView.as_view(), name="anime-list"),
    path("animes/create", AnimeCreateView.as_view(), name="anime-create"),
    path("animes/<int:pk>", AnimeDetailView.as_view(), name="anime-detail"),
    path("animes/<int:pk>/update", AnimeUpdateView.as_view(), name="anime-update"),
]
