from rest_framework.viewsets import GenericViewSet
from django.shortcuts import redirect
from django.urls import reverse

from airlines.models import (
    Country, City, Airport,
)
from airlines.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer
)
from airlines.mixins import GeneralMixin


class CountryViewSet(GeneralMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(GeneralMixin, GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AirportViewSet(GeneralMixin, GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
