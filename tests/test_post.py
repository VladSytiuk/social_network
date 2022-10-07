import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


URL_POSTS_LIST = reverse("posts-list")
URL_POST_DETAILS = reverse("posts-detail", kwargs={"pk": 1})

client = APIClient()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_post_success(authenticated_client, default_post_data):
    response = authenticated_client.post(
        URL_POSTS_LIST, data=default_post_data, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_post_not_authenticated_client_fail(
    authenticated_client, default_post_data
):
    response = client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_posts_list_success(authenticated_client, default_post_data):
    response = authenticated_client.get(URL_POSTS_LIST)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_posts_list_not_authenticated_client_fail(authenticated_client):
    response = client.get(URL_POSTS_LIST)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_post_details_success(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    response = authenticated_client.get(URL_POST_DETAILS)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_post_details_not_authenticated_client_fail(
    authenticated_client, default_post_data
):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    response = client.get(URL_POST_DETAILS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
