from django.db import models


class Country(models.Model):
    """
    Model that contain countries supported...
    by the service.
    """
    country = models.CharField(max_length=255)


class City(models.Model):
    """
    Model that contain supported cities in...
    supported counties.
    """
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Airport(models.Model):
    """
    Model that contain serviced airports.
    """
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Route(models.Model):
    """
    Model that contain flight routes with...
    departure and arrival points.
    """
    source = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True)
    distance = models.IntegerField()
