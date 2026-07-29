from django.urls import path
from .views import RandomFactView, FavoriteView, FavoriteListView, PopularFactListView

urlpatterns = [
    path(
        "random/",
        RandomFactView.as_view(),
        name="random-fact",
    ),
    path(
        "<int:pk>/favorite/",
        FavoriteView.as_view(),
        name="favorite-fact",
    ),
    path(
        "favorites/",
        FavoriteListView.as_view(),
        name="favorite-list",
    ),
    path(
        "popular/",
        PopularFactListView.as_view(),
        name="popular-facts",
    ),
]
