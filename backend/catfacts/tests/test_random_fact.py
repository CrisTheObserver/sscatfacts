from catfacts.models import CatFact
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catfacts.exceptions import CatFactServiceError


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
