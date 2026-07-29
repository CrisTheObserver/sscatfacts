from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .exceptions import CatFactServiceError
from .models import CatFact
from .serializers import CatFactSerializer
from .services import fetch_random_fact


class RandomFactView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            fact = fetch_random_fact()

        except CatFactServiceError:
            return Response(
                {
                    "detail": (
                        "The Cat Facts service is currently unavailable."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        fact, _ = CatFact.objects.get_or_create(
            fact=fact
        )
        serializer = CatFactSerializer(fact)

        return Response(serializer.data)