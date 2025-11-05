import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airlines.models import Country, City, Airport, Route


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_data(db):
    country_ua = Country.objects.create(country="Ukraine")
    country_pl = Country.objects.create(country="Poland")

    city_kyiv = City.objects.create(city="Kyiv", country=country_ua)
    city_warsaw = City.objects.create(city="Warsaw", country=country_pl)

    airport_iev = Airport.objects.create(name="IEV", city=city_kyiv)
    airport_waw = Airport.objects.create(name="WAW", city=city_warsaw)

    route = Route.objects.create(source=airport_iev, destination=airport_waw, distance=690)

    return {
        "countries": [country_ua, country_pl],
        "cities": [city_kyiv, city_warsaw],
        "airports": [airport_iev, airport_waw],
        "route": route,
    }


@pytest.mark.django_db
def test_country_list(api_client, sample_data):
    url = reverse("airlines:country-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["country"] == "Ukraine"


@pytest.mark.django_db
def test_city_create_and_retrieve(api_client, sample_data):
    country = sample_data["countries"][0]
    url = reverse("airlines:city-list")

    payload = {"city": "Lviv", "country": country.id}
    create_resp = api_client.post(url, payload)

    assert create_resp.status_code == status.HTTP_201_CREATED
    assert create_resp.data["city"] == "Lviv"
    assert create_resp.data["belonging_to"] == "Ukraine"


@pytest.mark.django_db
def test_airport_serializer_fields(api_client, sample_data):
    url = reverse("airlines:airport-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data[0]
    assert data["belonging_to"] == "Kyiv"
    assert data["country"] == "Ukraine"


@pytest.mark.django_db
def test_route_validation_same_source_and_destination(api_client, sample_data):
    airport = sample_data["airports"][0]
    url = reverse("airlines:route-list")
    payload = {"source": airport.id, "destination": airport.id, "distance": 100}

    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Source and destination cannot be the same" in str(response.data)


@pytest.mark.django_db
def test_route_list_and_filter(api_client, sample_data):
    url = reverse("airlines:route-list")

    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data[0]["from_"] == "IEV"
    assert resp.data[0]["to"] == "WAW"

    resp_filter = api_client.get(url, {"source_name": "IEV"})
    assert len(resp_filter.data) == 1
    assert resp_filter.data[0]["distance"] == 690
