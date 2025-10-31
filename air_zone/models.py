from django.db import models


class Crew(models.Model):
    """Model that include every pilot and flight attendant"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)



