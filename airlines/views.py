from rest_framework import generics
from django.shortcuts import redirect
from django.urls import reverse

from airlines.models import Country, City
from airlines.serializers import CountrySerializer, CitySerializer
from airlines.permissions import IsStaffOrReadOnly


class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsStaffOrReadOnly,)


class CountryDestroyView(generics.DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsStaffOrReadOnly,)


class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsStaffOrReadOnly,)


class CityDestroyView(generics.DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsStaffOrReadOnly,)
