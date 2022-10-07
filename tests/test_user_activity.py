import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


URL_USER_ACTIVITY = reverse("user-activity", kwargs={"pk": 1})

client = APIClient()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_user_activity_success(authenticated_client):
    response = authenticated_client.get(URL_USER_ACTIVITY)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_user_activity_not_authenticated_fail(authenticated_client):
    response = client.get(URL_USER_ACTIVITY)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
