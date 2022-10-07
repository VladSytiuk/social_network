import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


USER_MODEL = get_user_model()

URL_AUTH = reverse("token_obtain_pair")
URL_SIGN_UP = reverse("sign-up")

client = APIClient()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_jwt_token_success(default_user_data):
    client.post(URL_SIGN_UP, data=default_user_data, format="json")
    response = client.post(URL_AUTH, data=default_user_data, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_jwt_token_fail(default_user_data):
    response = client.post(URL_AUTH, data=default_user_data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
