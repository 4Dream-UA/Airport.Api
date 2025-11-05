from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, Ticket
from .serializers import OrderSerializer, TicketSerializer, TicketListSerializer
from airlines.mixins import GeneralMixin


class TicketViewSet(
    GeneralMixin,
    viewsets.GenericViewSet
):
    queryset = Ticket.objects.select_related("flight", "order", "flight__route")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TicketListSerializer
        return TicketSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route", "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
