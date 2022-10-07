import random

import pytest

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


USER_MODEL = get_user_model()


@pytest.fixture()
def default_user_data():
    return {
        "username": f"test_user{random.randint(1, 99999)}",
        "email": "test_mail@gmail.com",
        "password": "password",
    }


@pytest.fixture()
def authenticated_client(default_user_data):
    user = USER_MODEL.objects.create(**default_user_data, is_active=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def another_client(default_user_data):
    default_user_data["username"] = "another_test_user"
    user = USER_MODEL.objects.create(**default_user_data, is_active=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def default_post_data():
    return {"title": "test_title", "body": "body"}
