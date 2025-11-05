from django.urls import path, include
from rest_framework import routers

from .views import (
    OrderViewSet,
    TicketViewSet
)

app_name = "tickets"

router = routers.DefaultRouter()

router.register("orders", OrderViewSet)
router.register("buy", TicketViewSet)

urlpatterns = [path("", include(router.urls))]
