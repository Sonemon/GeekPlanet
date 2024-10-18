from django.urls import path
from .views import (
    add_friend,
    remove_friend,
    MainPageView,
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    UserListView,
    UserUpdateView,
    UserDetailView,
    AnimeListView,
    AnimeCreateView,
    AnimeDetailView,
    AnimeUpdateView,
    AnimeAddReviewView,
)

app_name = "geekplanet"

urlpatterns = [
    path("", MainPageView.as_view(), name="mainpage"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("geeks/", UserListView.as_view(), name="user-list"),
    path("geeks/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("geeks/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("geeks/<int:pk>/add/", add_friend, name="add-friend"),
    path("geeks/<int:pk>/remove/", remove_friend, name="remove-friend"),
    path("animes/", AnimeListView.as_view(), name="anime-list"),
    path("animes/create/", AnimeCreateView.as_view(), name="anime-create"),
    path("animes/<int:pk>/", AnimeDetailView.as_view(), name="anime-detail"),
    path("animes/<int:pk>/update/", AnimeUpdateView.as_view(), name="anime-update"),
    path("anime/<int:pk>/add-review/", AnimeAddReviewView.as_view(), name="anime-add-review"),
]
