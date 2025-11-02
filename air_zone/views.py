from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import status

from .models import (
    TypeReference,
    Type,
    Crew,
    Airplane,
)
from .serializers import (
    TypeReferenceSerializer,
    TypeSerializer,
    CrewSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
)
from airlines.mixins import GeneralMixin


class TypeReferenceViewSet(GeneralMixin, GenericViewSet):
    queryset = TypeReference.objects.all()
    serializer_class = TypeReferenceSerializer


class TypeViewSet(GeneralMixin, GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CrewViewSet(GeneralMixin, GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneViewSet(GeneralMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = AirplaneSerializer(airplane, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
