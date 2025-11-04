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
