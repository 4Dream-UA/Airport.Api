from django.db import models


class Crew(models.Model):
    """
    Model that include every pilot and flight
    (Meaning that include every member of crew)
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class TypeReference(models.Model):
    speed = models.IntegerField()
    distance = models.IntegerField()
    carrying = models.IntegerField()
    mass = models.IntegerField()
    height = models.IntegerField()
