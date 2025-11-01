from rest_framework import serializers
from django.urls import reverse

from .models import (
    Country, City, Airport,
)
from .mixins import DestroyLinkMixin


class CountrySerializer(DestroyLinkMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country', 'destroy_link']
        destroy_view_name = 'airlines:country_destroy'


class CitySerializer(DestroyLinkMixin, serializers.ModelSerializer):
    belonging_to = serializers.CharField(source="country.country", read_only=True)

    class Meta:
        model = City
        fields = ['id', 'city', 'country', 'belonging_to', 'destroy_link']
        extra_kwargs = {'country': {'write_only': True}}
        destroy_view_name = 'airlines:city_destroy'


class AirportSerializer(DestroyLinkMixin, serializers.ModelSerializer):
    belonging_to = serializers.CharField(source="city.city", read_only=True)
    country = serializers.CharField(source="city.country.country", read_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'belonging_to', 'country', 'city', 'destroy_link']
        extra_kwargs = {'city': {'write_only': True}}
        destroy_view_name = 'airlines:airport_destroy'
