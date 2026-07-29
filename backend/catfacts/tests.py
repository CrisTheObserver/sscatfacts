from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import CatFact, Favorite
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catfacts.exceptions import CatFactServiceError


class FavoriteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofia",
            password="password123",
        )

        self.fact = CatFact.objects.create(
            fact="Cats sleep around 16 hours a day."
        )

    def test_create_favorite(self):
        favorite = Favorite.objects.create(
            user=self.user,
            cat_fact=self.fact,
        )

        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.cat_fact, self.fact)

    def test_duplicate_favorite_not_allowed(self):
        Favorite.objects.create(
            user=self.user,
            cat_fact=self.fact,
        )

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                cat_fact=self.fact,
            )

class RandomFactViewTests(APITestCase):
    @patch("catfacts.views.fetch_random_fact")
    def test_get_random_fact(self, mock_fetch):
        mock_fetch.return_value = "Cats have five toes on their front paws."
        response = self.client.get(reverse("random-fact"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["fact"], mock_fetch.return_value)
        self.assertEqual(CatFact.objects.count(), 1)

    @patch("catfacts.views.fetch_random_fact")
    def test_random_fact_is_not_duplicated(self, mock_fetch):
        mock_fetch.return_value = "Cats purr."
        self.client.get(reverse("random-fact"))
        self.client.get(reverse("random-fact"))

        self.assertEqual(CatFact.objects.count(), 1)

    @patch("catfacts.views.fetch_random_fact")
    def test_returns_503_when_service_fails(self, mock_fetch):
        mock_fetch.side_effect = CatFactServiceError()
        response = self.client.get(reverse("random-fact"))

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )