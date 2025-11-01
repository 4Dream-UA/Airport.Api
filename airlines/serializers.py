from rest_framework import serializers
from django.urls import reverse

from .models import (
    Country, City, Airport,
    Route,
)
from .mixins import DestroyLinkMixin


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country', 'destroy_link']


class CitySerializer(serializers.ModelSerializer):
    belonging_to = serializers.CharField(source="country.country", read_only=True)

    class Meta:
        model = City
        fields = ['id', 'city', 'country', 'belonging_to']
        extra_kwargs = {'country': {'write_only': True}}


class AirportSerializer(serializers.ModelSerializer):
    belonging_to = serializers.CharField(source="city.city", read_only=True)
    country = serializers.CharField(source="city.country.country", read_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'belonging_to', 'country', 'city']
        extra_kwargs = {'city': {'write_only': True}}


class RouteSerializer(DestroyLinkMixin, serializers.ModelSerializer):
    from_ = serializers.CharField(source="source.name", read_only=True)
    to = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'from_', 'to', 'source', 'destination', 'distance', 'travel_date']
        extra_kwargs = {
            'source': {'write_only': True},
            'destination': {'write_only': True},
        }

    def validate(self, attrs):
        source = attrs.get('source')
        destination = attrs.get('destination')

        if source == destination:
            raise serializers.ValidationError("Source and destination cannot be the same!")

        return attrs