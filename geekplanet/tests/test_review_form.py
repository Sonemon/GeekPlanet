from django.test import TestCase
from geekplanet.models import User, Anime, AnimeType, Genre, Review
from geekplanet.forms import ReviewForm
from django.contrib.contenttypes.models import ContentType


class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.anime_type = AnimeType.objects.create(name="Action", anime_type_description="Action anime")
        self.genre = Genre.objects.create(name="Adventure")

        self.anime = Anime.objects.create(
            title="Test Anime",
            anime_type=self.anime_type,
            episodes=20,
            episode_duration=25,
            status="ongoing",
            description="This is a test anime.",
        )
        self.anime.genres.set([self.genre])

    def test_review_form_with_all_fields(self):
        form_data = {
            "content": "This is a great anime!",
            "rating": 8,
            "character": "positive",
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

        review = form.save(commit=False)
        review.user = self.user
        review.content_type = ContentType.objects.get_for_model(Anime)
        review.object_id = self.anime.id
        review.save()

        self.assertEqual(review.content, "This is a great anime!")

    def test_review_form_invalid(self):
        form_data = {
            "content": "",
            "rating": 11,
            "character": "positive",
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)
        self.assertIn("rating", form.errors)
