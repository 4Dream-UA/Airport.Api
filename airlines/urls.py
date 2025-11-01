from django.urls import path
from airlines.views import (
    CountryListCreateView,
    CountryDestroyView,
    CityListCreateView,
    CityDestroyView,
    AirportListCreateView,
    AirportDestroyView,
)

urlpatterns = [
    path("countries/", CountryListCreateView.as_view(), name="countries"),
    path("country_destroy/<int:pk>", CountryDestroyView.as_view(), name="country_destroy"),

    path("cities/", CityListCreateView.as_view(), name="cities"),
    path("city_destroy/<int:pk>", CityDestroyView.as_view(), name="city_destroy"),

    path("airports/", AirportListCreateView.as_view(), name="airports"),
    path("airport_destroy/<int:pk>", AirportDestroyView.as_view(), name="airport_destroy"),
]

app_name = "airlines"
