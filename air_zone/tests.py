import io
import pytest
from PIL import Image
from django.urls import reverse
from rest_framework import status

from air_zone.models import (
    Airplane,
    TypeReference,
    Type,
    Flight,
    Crew,
)
from airlines.models import Route


@pytest.fixture
def airplane_type():
    return Type.objects.create(name="Boeing")


@pytest.fixture
def crew():
    return Crew.objects.create(first_name="John", last_name="Miller")


@pytest.fixture
def type_reference():
    return TypeReference.objects.create(
        speed=900,
        distance=15000,
        carrying=20000,
        masa=80000,
        height=12000,
    )


@pytest.fixture
def airplane(airplane_type, type_reference):
    return Airplane.objects.create(
        name="Boeing 737",
        rows=30,
        seats=6,
        type=airplane_type,
        references=type_reference,
    )


@pytest.fixture
def flight(airplane, crew):
    source = Route.objects.create(source_name="Kyiv", destination_name="Berlin")
    flight = Flight.objects.create(
        route=source,
        airplane=airplane,
        departure_time="2025-11-05T10:00:00Z",
        arrival_time="2025-11-05T13:00:00Z",
    )
    flight.crew.add(crew)
    return flight


# ---------------------- TESTS START HERE ----------------------------


@pytest.mark.django_db
def test_create_airplane_with_reference(api_client, airplane_type):
    """Check airplane creating with TypeReference."""
    url = reverse("air_zone:airplane-list")
    payload = {
        "name": "Airbus A320",
        "rows": 28,
        "seats": 6,
        "type": airplane_type.id,
        "references": {
            "speed": 870,
            "distance": 12000,
            "carrying": 19000,
            "masa": 75000,
            "height": 11800
        }
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Airplane.objects.count() == 1
    airplane = Airplane.objects.first()
    assert airplane.references is not None
    assert airplane.references.speed == 870


@pytest.mark.django_db
def test_update_airplane_reference(api_client, airplane):
    """Check updating of Reference in airplane."""
    url = reverse("air_zone:airplane-detail", args=[airplane.id])
    payload = {
        "references": {
            "speed": 950,
            "distance": 16000,
            "carrying": 21000,
            "masa": 82000,
            "height": 12500,
        }
    }
    response = api_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    airplane.refresh_from_db()
    assert airplane.references.speed == 950
    assert airplane.references.distance == 16000


@pytest.mark.django_db
def test_upload_airplane_image(api_client, airplane):
    """Check upload-image action."""
    url = reverse("air_zone:airplane-upload-image", args=[airplane.id])

    image = Image.new("RGB", (100, 100))
    image_file = io.BytesIO()
    image.save(image_file, format="JPEG")
    image_file.name = "test.jpg"
    image_file.seek(0)

    response = api_client.post(url, {"image": image_file}, format="multipart")

    assert response.status_code == status.HTTP_200_OK
    airplane.refresh_from_db()
    assert airplane.image is not None


@pytest.mark.django_db
def test_create_flight_with_route_autocreate(api_client, airplane, crew):
    """Check flight creating with route."""
    url = reverse("air_zone:flight-list")
    payload = {
        "departure_time": "2025-11-05T09:00:00Z",
        "arrival_time": "2025-11-05T11:00:00Z",
        "airplane": airplane.id,
        "crew": [crew.id],
        "route_": {
            "source": {"name": "Warsaw"},
            "destination": {"name": "Prague"},
            "distance": 800
        }
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Flight.objects.count() == 1
    assert Route.objects.filter(source__name="Warsaw", destination__name="Prague").exists()


@pytest.mark.django_db
def test_flight_filter_by_source_and_destination(api_client, flight):
    """Filtering of flights with source and destination."""
    url = reverse("air_zone:flight-list")
    response = api_client.get(url, {"source_name": "Kyiv", "destination_name": "Berlin"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["from_"] == "Kyiv"
    assert response.data["results"][0]["to"] == "Berlin"
