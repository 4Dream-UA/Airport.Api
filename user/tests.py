import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:manage")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        email="test@example.com", password="testpass123"
    )


@pytest.mark.django_db
def test_user_registration_success(api_client):
    """Test creating user is successful"""
    payload = {"email": "new@example.com", "password": "strongpass123"}
    response = api_client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(email=payload["email"])
    assert user.check_password(payload["password"])
    assert "password" not in response.data


@pytest.mark.django_db
def test_user_registration_existing_email(api_client, user):
    """Test creating a user with existing email fails"""
    payload = {"email": user.email, "password": "pass12345"}
    response = api_client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_min_length(api_client):
    """Test password must be more than 5 characters"""
    payload = {"email": "short@example.com", "password": "123"}
    response = api_client.post(CREATE_USER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not get_user_model().objects.filter(email=payload["email"]).exists()


@pytest.mark.django_db
def test_retrieve_user_profile_authorized(api_client, user):
    """Test retrieving profile for logged in user"""
    api_client.force_authenticate(user=user)

    response = api_client.get(ME_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": user.id,
        "email": user.email,
        "is_staff": user.is_staff,
    }


@pytest.mark.django_db
def test_retrieve_user_unauthorized(api_client):
    """Test authentication is required for /me/ endpoint"""
    response = api_client.get(ME_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_password_update(api_client, user):
    """Test password is hashed on user update"""
    api_client.force_authenticate(user=user)
    payload = {"password": "newsecurepass123"}

    serializer_url = reverse("user:manage")
    response = api_client.patch(serializer_url, payload)

    user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert user.check_password(payload["password"])
