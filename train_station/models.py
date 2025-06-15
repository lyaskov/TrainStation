from django.db import models

from train_station_service import settings


class Station(models.Model):
    """
    Represents a railway station with a name and geographical coordinates.
    """

    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    """
    Represents a route between two stations, including distance in kilometers.
    """

    source = models.ForeignKey(
        Station, related_name="routes_from", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Station, related_name="routes_to", on_delete=models.CASCADE
    )
    distance = models.IntegerField(help_text="Distance in kilometers")

    def __str__(self):
        return f"{self.source} - {self.destination}"


class TrainType(models.Model):
    """
    Represents the type or category of a train.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Train(models.Model):
    """
    Represents a train, including its name, number of cargo units,
    places in each cargo, and associated train type.
    """

    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Crew(models.Model):
    """
    Represents a crew member, including their first and last name.
    Crew members can be assigned to multiple journeys (trips).
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Many-to-many to Journey (Trip), set below

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    """
    Represents a specific journey (trip) taken by a train on a route
    with departure and arrival times and assigned crew.
    """

    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    def __str__(self):
        return f"{self.route} ({self.departure_time:%Y-%m-%d %H:%M})"


class Order(models.Model):
    """
    Represents an order placed by a user, containing one or more tickets.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class Ticket(models.Model):
    """
    Represents a ticket for a specific seat in a cargo on a journey,
    linked to a specific order.
    """

    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket {self.id}: Journey {self.journey}, Cargo {self.cargo}, Seat {self.seat}"
