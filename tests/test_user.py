import pytest

from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse

URL_SIGN_UP = reverse("sign-up")

client = APIClient()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_sign_up_success(default_user_data):
    response = client.post(URL_SIGN_UP, data=default_user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_sign_up_with_not_unique_username_fail(default_user_data):
    client.post(URL_SIGN_UP, data=default_user_data, format="json")
    response = client.post(URL_SIGN_UP, data=default_user_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
