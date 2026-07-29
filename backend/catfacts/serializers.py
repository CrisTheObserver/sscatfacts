from rest_framework import serializers
from .models import CatFact


class CatFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatFact
        fields = ["id", "fact"]
        