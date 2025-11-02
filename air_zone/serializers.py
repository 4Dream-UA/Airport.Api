from rest_framework import serializers

from .models import TypeReference, Type, Crew, Airplane


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
    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats", "image", "type", "references"]
        extra_kwargs = {
            "type": {"write_only": True},
            "references": {"write_only": True},
        }


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
