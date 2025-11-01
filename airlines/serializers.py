from rest_framework import serializers
from django.urls import reverse

from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    destroy_link = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'country', 'destroy_link']

    def get_destroy_link(self, obj):
        return reverse('airlines:country_destroy', kwargs={'pk': obj.pk})
