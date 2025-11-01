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

    class Meta:
        model = City
        fields = ['id', 'city', 'country', 'destroy_link']

    def get_destroy_link(self, obj):
        return reverse('airlines:city_destroy', kwargs={'pk': obj.pk})
