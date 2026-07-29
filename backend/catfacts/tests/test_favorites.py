from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catfacts.models import CatFact, Favorite


class FavoriteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofia",
            password="password123",
        )
        self.fact = CatFact.objects.create(
            fact="Purring does not always indicate that a cat is happy and healthy - some cats will purr loudly when they are terrified or in pain."
        )
        self.url = reverse(
            "favorite-fact",
            kwargs={"pk": self.fact.pk},
        )

    def test_user_can_favorite_fact(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertTrue(response.data["favorite"])
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                cat_fact=self.fact,
            ).exists()
        )

    def test_user_can_unfavorite_fact(self):
        self.client.force_authenticate(user=self.user)
        Favorite.objects.create(
            user=self.user,
            cat_fact=self.fact,
        )
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertFalse(response.data["favorite"])
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                cat_fact=self.fact,
            ).exists()
        )

    def test_anonymous_user_cannot_favorite(self):
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_returns_404_when_fact_does_not_exist(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "favorite-fact",
            kwargs={"pk": 999},
        )
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class FavoriteListViewTests(APITestCase):
    def setUp(self):
        self.sofia = User.objects.create_user(
            username="sofia",
            password="password123",
        )
        self.maria = User.objects.create_user(
            username="maria",
            password="password321",
        )
        self.fact1 = CatFact.objects.create(
            fact="Purring does not always indicate that a cat is happy and healthy - some cats will purr loudly when they are terrified or in pain."
        )
        self.fact2 = CatFact.objects.create(
            fact="It has been scientifically proven that stroking a cat can lower one's blood pressure."
        )
        self.fact3 = CatFact.objects.create(
            fact="Cats spend nearly 1/3 of their waking hours cleaning themselves."
        )
        self.url = reverse("favorite-list")

    def test_returns_only_user_favorites(self):
        self.client.force_authenticate(user=self.sofia)
        Favorite.objects.create(
            user=self.sofia,
            cat_fact=self.fact1,
        )
        Favorite.objects.create(
            user=self.sofia,
            cat_fact=self.fact2,
        )
        Favorite.objects.create(
            user=self.maria,
            cat_fact=self.fact3,
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        facts = [fact["fact"] for fact in response.data]

        self.assertIn(self.fact1.fact, facts)
        self.assertIn(self.fact2.fact, facts)
        self.assertNotIn(self.fact3.fact, facts)

    def test_returns_empty_list_when_user_has_no_favorites(self):
        self.client.force_authenticate(user=self.sofia)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_anonymous_user_cannot_see_list_favorites(self):
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class PopularFactListViewTests(APITestCase):
    def setUp(self):
        self.sofia = User.objects.create_user(
            username="sofia",
            password="password123",
        )
        self.maria = User.objects.create_user(
            username="maria",
            password="password321",
        )
        self.jose = User.objects.create_user(
            username="jose",
            password="password213",
        )
        self.fact1 = CatFact.objects.create(
            fact="Purring does not always indicate that a cat is happy and healthy - some cats will purr loudly when they are terrified or in pain."
        )
        self.fact2 = CatFact.objects.create(
            fact="It has been scientifically proven that stroking a cat can lower one's blood pressure."
        )
        self.fact3 = CatFact.objects.create(
            fact="Cats spend nearly 1/3 of their waking hours cleaning themselves."
        )
        self.url = reverse("popular-facts")

    def test_returns_facts_ordered_by_number_of_favorites(self):
        Favorite.objects.create(
            user=self.sofia,
            cat_fact=self.fact1,
        )
        Favorite.objects.create(
            user=self.maria,
            cat_fact=self.fact1,
        )
        Favorite.objects.create(
            user=self.jose,
            cat_fact=self.fact1,
        )
        Favorite.objects.create(
            user=self.sofia,
            cat_fact=self.fact2,
        )
        Favorite.objects.create(
            user=self.maria,
            cat_fact=self.fact2,
        )
        Favorite.objects.create(
            user=self.sofia,
            cat_fact=self.fact3,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data[0]["fact"], self.fact1.fact)
        self.assertEqual(response.data[1]["fact"], self.fact2.fact)
        self.assertEqual(response.data[2]["fact"], self.fact3.fact)

        self.assertEqual(response.data[0]["favorites_count"], 3)
        self.assertEqual(response.data[1]["favorites_count"], 2)
        self.assertEqual(response.data[2]["favorites_count"], 1)
