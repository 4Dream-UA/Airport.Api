from django.db import models


class Country(models.Model):
    """
    Model that contain all countries supported...
    by the service.
    """
    country = models.CharField(max_length=255)
