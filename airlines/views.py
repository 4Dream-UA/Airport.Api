from rest_framework import generics
from django.shortcuts import redirect
from django.urls import reverse

from airlines.models import Country, City
from airlines.serializers import CountrySerializer, CitySerializer
from airlines.mixins import IsStaffOrReadOnlyMixin


class CountryListCreateView(IsStaffOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDestroyView(IsStaffOrReadOnlyMixin, generics.DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListCreateView(IsStaffOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityDestroyView(IsStaffOrReadOnlyMixin, generics.DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
