from rest_framework import serializers

from .models import TypeReference, Type, Crew


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
