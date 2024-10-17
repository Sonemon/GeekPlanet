import os
import random

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import AnimeForm, CustomUserCreationForm
from .models import User, Anime, AnimeType, Review


class BasePageMixin:
    area_name = "GeekPlanet"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        background_images_path = os.path.join(settings.BASE_DIR, "static", "img", "backgrounds")
        background_images = os.listdir(background_images_path)
        context["background_image"] = random.choice(background_images)
        context["current_area"] = self.area_name
        context["current_user"] = self.request.user
        return context


class MainPageView(BasePageMixin,
                   generic.TemplateView):
    template_name = "geekplanet/mainpage.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["latest_animes"] = Anime.objects.order_by("-id")[:5]
        return context


class CustomLoginView(BasePageMixin,
                      LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("geekplanet:mainpage"))
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(BasePageMixin,
                       LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("geekplanet:mainpage"))
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(BasePageMixin,
                         generic.TemplateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("geekplanet:mainpage")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self.form_class()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("geekplanet:mainpage"))
        return super().dispatch(request, *args, **kwargs)


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
