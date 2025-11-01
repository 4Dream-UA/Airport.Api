from django.db import models


class Country(models.Model):
    """
    Model that contain all countries supported...
    by the service.
    """
    country = models.CharField(max_length=255)


class City(models.Model):
    """
    Model that contain all supported cities in...
    supported counties.
    """
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
