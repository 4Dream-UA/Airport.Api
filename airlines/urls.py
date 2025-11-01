from django.urls import path
from airlines.views import CountryListCreateView, CountryDestroyView


urlpatterns = [
    path("countries/", CountryListCreateView.as_view(), name="countries"),
    path("country_destroy/<int:pk>", CountryDestroyView.as_view(), name="country_destroy"),
]

app_name = "airlines"
