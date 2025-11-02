from rest_framework import filters, permissions
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.shortcuts import redirect
from django.urls import reverse

from airlines.models import (
    Country, City, Airport,
    Route,
)
from airlines.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer, RouteDetailSerializer,
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


class RouteFilter(FilterSet):
    source_name = CharFilter(field_name='source__name', lookup_expr='icontains')
    destination_name = CharFilter(field_name='destination__name', lookup_expr='icontains')

    class Meta:
        model = Route
        fields = ['source_name', 'destination_name']


class RouteViewSet(GeneralMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RouteFilter
    ordering_fields = ['distance']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer
