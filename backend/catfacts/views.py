from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .exceptions import CatFactServiceError
from .models import CatFact, Favorite
from .serializers import CatFactSerializer
from .services import fetch_random_fact


class RandomFactView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            fact_text = fetch_random_fact()

        except CatFactServiceError:
            return Response(
                {"detail": ("The Cat Facts service is currently unavailable.")},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        fact, _ = CatFact.objects.get_or_create(fact=fact_text)
        serializer = CatFactSerializer(fact)

        return Response(serializer.data)


class FavoriteView(APIView):
    def post(self, request, pk):
        cat_fact = get_object_or_404(CatFact, pk=pk)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            cat_fact=cat_fact,
        )

        if created:
            return Response(
                {"favorite": True},
                status=status.HTTP_200_OK,
            )
        favorite.delete()
        return Response(
            {"favorite": False},
            status=status.HTTP_200_OK,
        )


class FavoriteListView(APIView):
    def get(self, request):

        facts = (
            CatFact.objects.filter(favorites__user=request.user)
            .annotate(favorites_count=Count("favorites"))
            .order_by("-favorites_count", "fact")
        )

        serializer = CatFactSerializer(
            facts,
            many=True,
        )

        return Response(serializer.data)


class PopularFactListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        facts = CatFact.objects.annotate(favorites_count=Count("favorites")).order_by(
            "-favorites_count", "fact"
        )

        serializer = CatFactSerializer(
            facts,
            many=True,
        )

        return Response(serializer.data)
