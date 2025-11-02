from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import TypeReference
from .serializers import TypeReferenceSerializer
from airlines.mixins import GeneralMixin


class TypeReferenceViewSet(GeneralMixin, GenericViewSet):
    queryset = TypeReference.objects.all()
    serializer_class = TypeReferenceSerializer
