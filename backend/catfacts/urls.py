from django.urls import path
from .views import RandomFactView


urlpatterns = [
    path(
        "random/",
        RandomFactView.as_view(),
        name="random-fact",
    ),
]