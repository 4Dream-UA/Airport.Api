from rest_framework import serializers
from django.urls import reverse

from .models import Country, City


class CountrySerializer(serializers.ModelSerializer):
    destroy_link = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'country', 'destroy_link']

    def get_destroy_link(self, obj):
        return reverse('airlines:country_destroy', kwargs={'pk': obj.pk})


class CitySerializer(serializers.ModelSerializer):
    destroy_link = serializers.SerializerMethodField()
    belonging_to = serializers.CharField(source="country.country", read_only=True)

    class Meta:
        model = City
        fields = ['id', 'city', 'country', 'belonging_to', 'destroy_link']
        extra_kwargs = {'country': {'write_only': True}}

    def get_destroy_link(self, obj):
        return reverse('airlines:city_destroy', kwargs={'pk': obj.pk})
