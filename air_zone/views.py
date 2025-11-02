from rest_framework.viewsets import GenericViewSet

from .models import (
    TypeReference,
    Type
)
from .serializers import TypeReferenceSerializer, TypeSerializer
from airlines.mixins import GeneralMixin


class TypeReferenceViewSet(GeneralMixin, GenericViewSet):
    queryset = TypeReference.objects.all()
    serializer_class = TypeReferenceSerializer


class TypeViewSet(GeneralMixin, GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
