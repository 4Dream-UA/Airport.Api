from rest_framework.reverse import reverse
from rest_framework import serializers, mixins

from airlines.permissions import IsStaffOrReadOnly


class DestroyLinkMixin(serializers.Serializer):
    destroy_link = serializers.SerializerMethodField()

    def get_destroy_link(self, obj):
        view_name = getattr(self.Meta, "destroy_view_name", None)
        if not view_name:
            raise AttributeError(
                f"{self.__class__.__name__} must define Meta.destroy_view_name"
            )
        return reverse(view_name, kwargs={'pk': obj.pk})


class IsStaffOrReadOnlyMixin:
    permission_classes = (IsStaffOrReadOnly,)


class GeneralMixin(
    IsStaffOrReadOnlyMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    pass
