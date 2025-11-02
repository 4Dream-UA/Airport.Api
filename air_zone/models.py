from django.db import models

from .extra_scripts.get_image_path_for_db_model import get_image_path_for_db_model
from airlines.models import Route


class Crew(models.Model):
    """
    Model that include every pilot and flight
    (Meaning that include every member of crew).
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class TypeReference(models.Model):
    """
    Model that include main references of airplane:
    speed, distance, carrying, masa, height.
    """
    speed = models.IntegerField()
    distance = models.IntegerField()
    carrying = models.IntegerField()
    masa = models.IntegerField()
    height = models.IntegerField()


class Type(models.Model):
    """
    Model that include type of airplane, such as:
    narrow-body, wide-body, etc.
    """
    name = models.CharField(max_length=255)


class Airplane(models.Model):
    """
    Model that include unique/important airplane information.
    """
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats = models.IntegerField()
    image = models.ImageField(upload_to=get_image_path_for_db_model)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    references = models.OneToOneField(TypeReference, on_delete=models.SET_NULL, null=True)


class Flight(models.Model):
    """
    Model that include flight information.
    """
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.SET_NULL, null=True)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
