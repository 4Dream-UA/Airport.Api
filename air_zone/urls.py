from django.urls import path, include
from rest_framework import routers

from air_zone.views import TypeReferenceViewSet

app_name = "air_zone"

router = routers.DefaultRouter()

router.register("references", TypeReferenceViewSet)


urlpatterns = [path("", include(router.urls))]
