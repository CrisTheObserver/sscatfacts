from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from catfacts.models import CatFact, Favorite


class FavoriteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sofia",
            password="password123",
        )

        self.fact = CatFact.objects.create(fact="Cats sleep around 16 hours a day.")

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
