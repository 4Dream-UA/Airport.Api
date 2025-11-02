from django.urls import path, include
from rest_framework import routers

from air_zone.views import (
    TypeReferenceViewSet,
    TypeViewSet, CrewViewSet,
)

app_name = "air_zone"

router = routers.DefaultRouter()

router.register("references", TypeReferenceViewSet)
router.register("types", TypeViewSet)
router.register("pilots", CrewViewSet)


urlpatterns = [path("", include(router.urls))]
