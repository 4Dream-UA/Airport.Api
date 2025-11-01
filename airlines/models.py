from django.db import models


class Country(models.Model):
    """
    Model that contain countries supported...
    by the service.
    """
    country = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.country


class City(models.Model):
    """
    Model that contain supported cities in...
    supported counties.
    """
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.city


class Airport(models.Model):
    """
    Model that contain serviced airports.
    """
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.city.city})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['city', 'name'], name='unique_airport')
        ]


class ActiveRouteManager(models.Manager):
    """
    Manager for active routes.
    """
    def get_queryset(self):
        return super().get_queryset().filter(travel_date__gte=timezone.now())

class PassiveRouteManager(models.Manager):
    """
    Manager for no active routes.
    """
    def get_queryset(self):
        return super().get_queryset().filter(travel_date__lt=timezone.now())


class Route(models.Model):
    """
    Model that contain flight routes with...
    departure and arrival points.
    """
    source = models.ForeignKey(
        Airport,
        on_delete=models.SET_NULL,
        null=True,
        related_name='route_source',
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.SET_NULL,
        null=True,
        related_name='route_destination',
    )
    distance = models.IntegerField()
    travel_date = models.DateTimeField(null=True)

    # Managers
    objects = models.Manager()          # build-in
    active = ActiveRouteManager()       # only active routes
    passive = PassiveRouteManager()     # only passive routes

    def __str__(self):
        return (
            f"{self.source.city.city} -> {self.destination.city.city}"
            f"({self.source} -> {self.destination}) => {self.distance}"
        )
