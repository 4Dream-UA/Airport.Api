from django.urls import path, include
from rest_framework import routers

from airlines.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    RouteViewSet,
    RoutePassiveViewSet,
)

app_name = "airlines"

router = routers.DefaultRouter()

router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("routes_passive", RoutePassiveViewSet, basename="route_passive")


urlpatterns = [path("", include(router.urls))]
