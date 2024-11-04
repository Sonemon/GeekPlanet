from django.test import TestCase
from geekplanet.models import AnimeType, Genre
from geekplanet.forms import AnimeForm


class AnimeFormTests(TestCase):
    def setUp(self):
        self.anime_type = AnimeType.objects.create(name="Action", anime_type_description="Action anime")
        self.genre = Genre.objects.create(name="Adventure")

        self.form_data = {
            "title": "Test Anime",
            "anime_type": self.anime_type,
            "episodes": 20,
            "episode_duration": 25,
            "genres": [self.genre],
            "status": "ongoing",
            "description": "This is a test anime.",
        }

    def test_anime_creation_form_with_all_fields(self):
        form = AnimeForm(data=self.form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        anime = form.save()
        self.assertEqual(anime.title, self.form_data["title"])
        self.assertEqual(anime.anime_type, self.form_data["anime_type"])
        self.assertEqual(anime.episodes, self.form_data["episodes"])
        self.assertEqual(anime.episode_duration, self.form_data["episode_duration"])
        self.assertEqual(anime.status, self.form_data["status"])
        self.assertEqual(anime.description, self.form_data["description"])
