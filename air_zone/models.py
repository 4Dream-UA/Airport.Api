from django.db import models


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
    speed, distance, carrying, mass, height.
    """
    speed = models.IntegerField()
    distance = models.IntegerField()
    carrying = models.IntegerField()
    mass = models.IntegerField()
    height = models.IntegerField()


class Type(models.Model):
    """
    Model that include type of airplane, such as:
    narrow-body, wide-body, etc.
    """
    name = models.CharField(max_length=255)
    type_reference = models.ForeignKey(TypeReference, on_delete=models.CASCADE)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats = models.IntegerField()
    image = models.ImageField(upload_to='airplane/images/')