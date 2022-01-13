from django.contrib.auth.models import User
from django.test import TestCase

from .forms import CreateUserForm, LoginUserForm, CreateUrlForm
from .models import Url


class Url_model_test(TestCase):
    def setUp(self) -> None:
        Url.objects.create(full_url="https://www.google.com")

    def test_hash_url_exists(self):
        qs = Url.objects.get(full_url="https://www.google.com")
        self.assertIsInstance(qs.hash_url, str)

    def test_clicks(self):
        qs = Url.objects.get(full_url="https://www.google.com")
        response = self.client.get(f'/{qs.hash_url}/')
        self.assertEqual(response.status_code, 302)
        qs_updated = Url.objects.get(hash_url=qs.hash_url)
        self.assertEqual(qs_updated.clicks, 1)


class CreateUserForm_form_test(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="test_user", email="exists@gmail.com", password="tu123456")

    def test_input_valid(self):
        form = CreateUserForm(
            data={
                "username": "tu",
                "email": "tu@gmail.com",
                "password1": "tu123456",
                "password2": "tu123456",
            }
        )
        self.assertTrue(form.is_valid())

    def test_input_invalid(self):
        form = CreateUserForm(
            data={
                "username": "",
                "email": "",
                "password1": "",
                "password2": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_email_exists(self):
        form = CreateUserForm(
            data={
                "username": "tu123",
                "email": "exists@gmail.com",
                "password1": "tu123456",
                "password2": "tu123456",
            }
        )
        self.assertFalse(form.is_valid())


class LoginUserForm_test_form(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="tu", email="tu@gmail.com", password="tu123456")

    def test_input_valid(self):
        form = LoginUserForm(data={"username": "tu", "password": "tu123456"})
        self.assertTrue(form.is_valid())

    def test_input_invalid(self):
        form = LoginUserForm(data={"username": "", "password": ""})
        self.assertFalse(form.is_valid())


class CreateUrlForm_test_form(TestCase):
    def test_input_valid(self):
        form = CreateUrlForm(data={"full_url": "https://www.google.com"})
        self.assertTrue(form.is_valid())

    def test_input_invalid(self):
        form = CreateUrlForm(data={"full_url": ""})
        self.assertFalse(form.is_valid())
