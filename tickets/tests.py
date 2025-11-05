import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tickets.models import Ticket, Order
from air_zone.models import Flight, Airplane
from airlines.models import Country, City, Airport, Route
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = get_user_model().objects.create_user(
        email="test@example.com", password="testpass123"
    )
    return user


@pytest.fixture
def setup_data(db):
    country = Country.objects.create(country="Ukraine")
    city = City.objects.create(city="Kyiv", country=country)
    airport = Airport.objects.create(name="IEV", city=city)

    country2 = Country.objects.create(country="Poland")
    city2 = City.objects.create(city="Warsaw", country=country2)
    airport2 = Airport.objects.create(name="WAW", city=city2)

    route = Route.objects.create(source=airport, destination=airport2, distance=690)
    airplane = Airplane.objects.create(model="Boeing 737", rows=10, seats=6)
    flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time="2025-12-01T12:00:00Z",
        arrival_time="2025-12-01T13:30:00Z",
    )

    return {"route": route, "flight": flight, "airplane": airplane}


@pytest.mark.django_db
def test_ticket_purchase_success(api_client, user, setup_data):
    api_client.force_authenticate(user=user)
    flight = setup_data["flight"]
    url = reverse("tickets:buy-list")

    payload = {"row": 3, "seat": 2, "flight": flight.id}
    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_201_CREATED
    ticket = Ticket.objects.first()
    assert ticket.row == 3
    assert ticket.order.user == user
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_ticket_validation_out_of_range(api_client, user, setup_data):
    api_client.force_authenticate(user=user)
    flight = setup_data["flight"]
    url = reverse("tickets:buy-list")

    payload = {"row": 99, "seat": 1, "flight": flight.id}
    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "out of range" in str(response.data)


@pytest.mark.django_db
def test_ticket_validation_already_taken(api_client, user, setup_data):
    api_client.force_authenticate(user=user)
    flight = setup_data["flight"]
    Ticket.objects.create(row=1, seat=1, flight=flight, order=Order.objects.create(user=user))
    url = reverse("tickets:buy-list")

    payload = {"row": 1, "seat": 1, "flight": flight.id}
    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already taken" in str(response.data)


@pytest.mark.django_db
def test_ticket_list_returns_flight_info(api_client, user, setup_data):
    api_client.force_authenticate(user=user)
    flight = setup_data["flight"]
    order = Order.objects.create(user=user)
    Ticket.objects.create(row=5, seat=4, flight=flight, order=order)

    url = reverse("tickets:buy-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data[0]["flight_info"]
    assert data["from"] == "IEV"
    assert data["to"] == "WAW"
    assert "departure" in data
    assert "arrival" in data


@pytest.mark.django_db
def test_order_list_for_user(api_client, user, setup_data):
    api_client.force_authenticate(user=user)
    flight = setup_data["flight"]

    order1 = Order.objects.create(user=user)
    Ticket.objects.create(row=2, seat=3, flight=flight, order=order1)

    url = reverse("tickets:orders-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert "tickets" in response.data[0]
    assert response.data[0]["tickets"][0]["row"] == 2
