from django.urls import path
from airlines.views import (
    CountryListCreateView,
    CountryDestroyView,
    CityListCreateView
)

urlpatterns = [
    path("countries/", CountryListCreateView.as_view(), name="countries"),
    path("country_destroy/<int:pk>", CountryDestroyView.as_view(), name="country_destroy"),

    path("cities/", CityListCreateView.as_view(), name="cities"),
]

app_name = "airlines"
