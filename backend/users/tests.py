from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache
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


class LoginTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="sofia",
            password="password123",
        )

    def test_login_success(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "sofia",
                "password": "password123",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "sofia",
                "password": "wrongpassword",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_login_rate_limit(self):
        for _ in range(10):
            response = self.client.post(
                "/api/auth/login/",
                {
                    "username": "sofia",
                    "password": "wrongpassword",
                },
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "sofia",
                "password": "wrongpassword",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
        )
