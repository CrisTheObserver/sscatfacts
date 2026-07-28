from django.contrib import admin
from .models import CatFact, Favorite


@admin.register(CatFact)
class CatFactAdmin(admin.ModelAdmin):
    list_display = ("id", "fact")
    search_fields = ("fact",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "cat_fact")