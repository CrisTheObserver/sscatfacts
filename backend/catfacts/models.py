from django.db import models
from django.contrib.auth.models import User


class CatFact(models.Model):
    fact = models.TextField(unique=True)

    def __str__(self):
        return self.fact[:50]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    cat_fact = models.ForeignKey(
        CatFact,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cat_fact"],
                name="unique_user_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user.username} liked '{self.cat_fact.fact[:30]}...'"
