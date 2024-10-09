import os
import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import AnimeForm
from .models import User, Anime, AnimeType, Review


class BasePageMixin:
    area_name = "GeekPlanet"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["current_area"] = self.area_name
        context["current_user"] = self.request.user

        # random backgroud from static
        background_images_path = os.path.join(settings.BASE_DIR, "static", "img", "backgrounds")
        background_images = os.listdir(background_images_path)
        context["background_image"] = random.choice(background_images)
        return context


class MainPageView(BasePageMixin,
                   generic.TemplateView):
    template_name = "geekplanet/mainpage.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["latest_animes"] = Anime.objects.order_by("-id")[:5]
        return context


class UserListView(LoginRequiredMixin,
                   BasePageMixin,
                   generic.ListView):
    model = User
    paginate_by = 10
    template_name = "geekplanet/user_list.html"
    area_name = "Geeks"


class UserDetailView(LoginRequiredMixin,
                     BasePageMixin,
                     generic.DetailView):
    model = User
    area_name = "Geeks"


class AnimeListView(BasePageMixin,
                    generic.ListView):
    model = Anime
    paginate_by = 20
    template_name = "geekplanet/anime_list.html"
    area_name = "Animes"


class AnimeCreateView(LoginRequiredMixin,
                      BasePageMixin,
                      generic.CreateView):
    model = Anime
    form_class = AnimeForm
    template_name = "geekplanet/anime_form.html"
    area_name = "Animes"
    success_url = reverse_lazy("geekplanet:anime-list")


class AnimeDetailView(BasePageMixin,
                      generic.DetailView):
    model = Anime
    area_name = "Animes"


class AnimeUpdateView(LoginRequiredMixin,
                      BasePageMixin,
                      generic.UpdateView):
    model = Anime
    form_class = AnimeForm
    template_name = "geekplanet/anime_form.html"
    success_url = reverse_lazy("geekplanet:anime-list")
