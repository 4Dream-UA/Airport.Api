from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    """
    Model to hold information about the user order's.
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
