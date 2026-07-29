import requests
from django.conf import settings
from .exceptions import CatFactServiceError

def fetch_random_fact():
    try:
        response = requests.get(
            settings.CATFACT_API_URL,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        return data["fact"]

    except requests.RequestException as exc:
        raise CatFactServiceError(
            "Unable to fetch a cat fact."
        ) from exc