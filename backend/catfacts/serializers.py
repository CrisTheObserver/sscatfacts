from rest_framework import serializers
from .models import CatFact


class CatFactSerializer(serializers.ModelSerializer):
    favorites_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CatFact
        fields = (
            "id",
            "fact",
            "favorites_count",
        )
