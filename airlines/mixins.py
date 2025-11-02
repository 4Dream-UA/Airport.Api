from rest_framework.reverse import reverse
from rest_framework import serializers, mixins

from airlines.permissions import IsStaffIfAuthenticatedReadOnly


class IsStaffIfAuthenticatedReadOnlyMixin:
    permission_classes = (IsStaffIfAuthenticatedReadOnly,)


class GeneralMixin(
    IsStaffIfAuthenticatedReadOnlyMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    pass
