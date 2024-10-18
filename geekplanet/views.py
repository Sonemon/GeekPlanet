import os
import random

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import AnimeForm, UserForm, ReviewForm
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
        context["is_moderator"] = self.request.user.groups.filter(name="Moderators").exists()
        return context


class ModeratorGroupRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name="Moderators").exists()

    def handle_no_permission(self):
        return redirect(reverse_lazy("geekplanet:mainpage"))


class MainPageView(BasePageMixin,
                   generic.TemplateView):
    template_name = "geekplanet/mainpage.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["latest_animes"] = Anime.objects.order_by("-id")[:4]
        context["num_animes"] = Anime.objects.count()
        context["num_geeks"] = User.objects.count()
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
    form_class = UserForm
    success_url = reverse_lazy("geekplanet:mainpage")

    def get(self, request, *args, **kwargs):
        form = self.form_class(is_update=False)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, is_update=False)
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


class UserUpdateView(LoginRequiredMixin,
                     BasePageMixin,
                     generic.UpdateView):
    model = User
    form_class = UserForm

    def dispatch(self, request, *args, **kwargs):
        is_moderator = request.user.groups.filter(name="Moderators").exists()
        user_to_update = self.get_object()

        if request.user != user_to_update and not is_moderator:
            return redirect(reverse_lazy("geekplanet:mainpage"))

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form_class = form_class or self.get_form_class()
        form_kwargs = self.get_form_kwargs()
        form_kwargs["is_update"] = True
        return form_class(**form_kwargs)

    def get_success_url(self):
        return reverse_lazy("geekplanet:user-detail", kwargs={"pk": self.request.user.id})


class AnimeListView(BasePageMixin,
                    generic.ListView):
    model = Anime
    paginate_by = 20
    template_name = "geekplanet/anime_list.html"
    area_name = "Animes"


class AnimeCreateView(LoginRequiredMixin,
                      ModeratorGroupRequiredMixin,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(
            content_type=ContentType.objects.get_for_model(Anime),
            object_id=self.object.id
        )

        user_reviewed = context["reviews"].filter(
            user=self.request.user).exists() if self.request.user.is_authenticated else False
        context["user_reviewed"] = user_reviewed

        return context


class AnimeUpdateView(LoginRequiredMixin,
                      ModeratorGroupRequiredMixin,
                      BasePageMixin,
                      generic.UpdateView):
    model = Anime
    form_class = AnimeForm
    template_name = "geekplanet/anime_form.html"
    success_url = reverse_lazy("geekplanet:anime-list")


class AnimeAddReviewView(LoginRequiredMixin, BasePageMixin, generic.CreateView):
    form_class = ReviewForm
    template_name = "geekplanet/anime-add-review.html"

    def get_anime(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Anime, pk=pk)

    def form_valid(self, form):
        anime = self.get_anime()
        review = form.save(commit=False)
        review.user = self.request.user
        review.content_type = ContentType.objects.get_for_model(anime)
        review.object_id = anime.id

        review.clean(user=self.request.user)

        review.save()
        return redirect("geekplanet:anime-detail", pk=anime.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["anime"] = self.get_anime()
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)
