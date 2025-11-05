from rest_framework import serializers
from django.db import transaction
from .models import Ticket, Order
from air_zone.models import Flight


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight"]
        extra_kwargs = {"flight": {"write_only": True}}

    def validate(self, attrs):
        flight = attrs["flight"]
        airplane = flight.airplane

        if not (1 <= attrs["row"] <= airplane.rows and 1 <= attrs["seat"] <= airplane.seats):
            raise serializers.ValidationError("Seat or row number is out of range.")

        if Ticket.objects.filter(
            flight=flight, row=attrs["row"], seat=attrs["seat"]
        ).exists():
            raise serializers.ValidationError("This seat is already taken for this flight.")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user

        with transaction.atomic():
            order = Order.objects.create(user=user)
            ticket = Ticket.objects.create(order=order, **validated_data)
        return ticket


class TicketListSerializer(TicketSerializer):
    flight_info = serializers.SerializerMethodField(read_only=True)

    class Meta(TicketSerializer.Meta):
        fields = ["id", "row", "seat", "flight_info"]

    def get_flight_info(self, obj):
        route = obj.flight.route
        return {
            "from": route.source.name if route else None,
            "to": route.destination.name if route else None,
            "departure": obj.flight.departure_time,
            "arrival": obj.flight.arrival_time,
        }


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True, source="ticket_set")

    class Meta:
        model = Order
        fields = ["id", "created", "tickets"]
