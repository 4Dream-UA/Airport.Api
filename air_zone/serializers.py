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
        fields = ["id", "name", "rows", "seats", "image", "type"]
        extra_kwargs = {"type": {"write_only": True}, "type_reference": {"write_only": True}}


class AirplaneListSerializer(serializers.ModelSerializer):
    types = serializers.CharField(many=True, source="airplane.type", read_only=True)

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats", "image", "types", "type", "type_reference"]
