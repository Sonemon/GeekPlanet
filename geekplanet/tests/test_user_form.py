from django.test import TestCase
from geekplanet.models import User
from geekplanet.forms import UserForm


class UserFormTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="existing_user", password="Password123!")

        self.form_data = {
            "username": "test_user",
            "password1": "Password_test!",
            "password2": "Password_test!",
            "email": "test@example.com",
            "first_name": "test_first",
            "last_name": "test_last",
            "bio": "Test user bio"
        }

    def test_user_creation_form_with_all_firlds(self):
        form = UserForm(data=self.form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_password_do_not_match(self):
        form_data = self.form_data
        form_data["password2"] = "Different_password!"
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_required_fields(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)

    def test_email_invalid_format(self):
        form_data = self.form_data.copy()
        form_data["email"] = "not-an-email"
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_username_unique(self):
        form_data = self.form_data.copy()
        form_data["username"] = "existing_user"
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
