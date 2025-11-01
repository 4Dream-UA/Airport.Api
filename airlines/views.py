from rest_framework import generics
from django.shortcuts import redirect
from django.urls import reverse

from airlines.models import Country
from airlines.serializers import CountrySerializer
from airlines.permissions import IsStaffOrReadOnly


class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsStaffOrReadOnly,)

    def create(self, request, *args, **kwargs):
        url = reverse('airlines:countries')
        redirect(url)
        return super().create(request, *args, **kwargs)

class CountryDestroyView(generics.DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsStaffOrReadOnly,)
