from rest_framework import serializers

from .models import (
    TypeReference,
    Type,
    Crew,
    Airplane,
    Flight
)
from airlines.serializers import RouteSerializer
from airlines.models import Route


class TypeReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeReference
        fields = ["id", "speed", "distance", "carrying", "masa", "height"]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["id", "name"]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class AirplaneSerializer(serializers.ModelSerializer):
    references = TypeReferenceSerializer()

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats", "image", "type", "references"]
        extra_kwargs = {
            "references": {"write_only": True},
        }


    def create(self, validated_data):
        reference_data = validated_data.pop("references", None)
        airplane = Airplane.objects.create(**validated_data)

        if reference_data:
            reference = TypeReference.objects.create(**reference_data)
            airplane.references = reference
            airplane.save()

        return airplane

    def update(self, instance, validated_data):
        image = validated_data.get("image", None)
        if image is None:
            validated_data["image"] = instance.image

        reference_data = validated_data.pop("references", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if reference_data:
            if hasattr(instance, "references") and instance.references:
                for field, value in reference_data.items():
                    setattr(instance.references, field, value)
                instance.references.save()
            else:
                instance.references = TypeReference.objects.create(**reference_data)
                instance.save()

        return instance


class AirplaneListSerializer(serializers.ModelSerializer):
    types = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats", "image", "types"]


class AirplaneDetailSerializer(serializers.ModelSerializer):
    types = serializers.CharField(source="type.name", read_only=True)
    references = TypeReferenceSerializer(read_only=True)

    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "rows",
            "seats",
            "image",
            "types",
            "references",
        ]


class FlightSerializer(serializers.ModelSerializer):
    route_ = RouteSerializer(write_only=True)
    from_ = serializers.CharField(source="route.source.name", read_only=True)
    to = serializers.CharField(source="route.destination.name", read_only=True)
    distance = serializers.CharField(source="route.distance", read_only=True)
    airplane_ = serializers.CharField(source="airplane.name", read_only=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "from_",
            "to",
            "airplane_",
            "distance",
            "departure_time",
            "arrival_time",
            "airplane",
            "crew",
            "route_",
        ]

        extra_kwargs = {
            "crew": {"write_only": True},
            "airplane": {"write_only": True},
        }

    def create(self, validated_data):
        route_data = validated_data.pop("route_", None)
        crew_data = validated_data.pop("crew", [])

        route = None
        if route_data:
            source = route_data.get("source")
            destination = route_data.get("destination")

            route, _ = Route.objects.get_or_create(
                source=source,
                destination=destination,
                defaults=route_data,
            )

        flight = Flight.objects.create(route=route, **validated_data)

        if crew_data:
            flight.crew.set(crew_data)

        return flight
