from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterTests(APITestCase):

    def test_register_user_success(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "sofia",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_short_password(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "sofia",
                "password": "pass",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(
            username="sofia",
            password="password123",
        )

        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "sofia",
                "password": "anotherpassword123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
