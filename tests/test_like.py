import datetime

import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


URL_POSTS_LIST = reverse("posts-list")
URL_LIKE_DETAILS = reverse("likes-detail", kwargs={"pk": 1})
URL_LIKES_LIST = reverse("likes-list")
URL_LIKES_ANALYTIC = reverse("analytic")


client = APIClient()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_like_success(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    response = authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_like_twice_fail(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    response = authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_like_not_authenticated_fail(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    response = client.post(URL_LIKES_LIST, data={"post": 1})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_like_success(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    response = authenticated_client.delete(URL_LIKE_DETAILS)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_like_not_authenticated_fail(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    response = client.delete(URL_LIKE_DETAILS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_someone_elses_like_fail(
    authenticated_client, another_client, default_post_data
):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    response = another_client.delete(URL_LIKE_DETAILS)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_likes_analytic_success(authenticated_client, default_post_data):
    authenticated_client.post(URL_POSTS_LIST, data=default_post_data, format="json")
    authenticated_client.post(URL_LIKES_LIST, data={"post": 1})
    date_end = datetime.date.today()
    response = authenticated_client.get(
        URL_LIKES_ANALYTIC, data={"date_start": "2022-10-04", "date_end": date_end}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["total_likes"] == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_likes_analytic_not_authenticated_fail():
    date_end = datetime.date.today()
    response = client.get(
        URL_LIKES_ANALYTIC, data={"date_from": "2022-10-04", "date_to": date_end}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
