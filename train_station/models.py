from django.db import models

from train_station_service import settings


class Station(models.Model):
    """
    Represents a railway station with a name and geographical coordinates.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Station name",
        help_text="The official name of the railway station (e.g., 'Kyiv').",
    )
    latitude = models.FloatField(
        help_text="Latitude of the station in decimal degrees (e.g., 50.4501)"
    )
    longitude = models.FloatField(
        help_text="Longitude of the station in decimal degrees (e.g., 30.5234)"
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    """
    Represents a route between two stations, including the distance in kilometers.
    """

    source = models.ForeignKey(
        Station,
        related_name="routes_from",
        on_delete=models.CASCADE,
        verbose_name="Source station",
        help_text="Starting station of the route (select station ID).",
    )
    destination = models.ForeignKey(
        Station,
        related_name="routes_to",
        on_delete=models.CASCADE,
        verbose_name="Destination station",
        help_text="Ending station of the route (select station ID).",
    )
    distance = models.IntegerField(
        verbose_name="Distance (km)",
        help_text="Distance between the stations in kilometers.",
    )

    def __str__(self):
        return f"{self.source} - {self.destination}"


class TrainType(models.Model):
    """
    Represents the type or category of a train (e.g., Intercity, Regional).
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Train type name",
        help_text="Name of the train type or category (e.g., 'Intercity', 'Regional').",
    )

    def __str__(self):
        return self.name


class Train(models.Model):
    """
    Represents a train, including its name, number of cargo units,
    number of seats in each cargo, and associated train type.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Train name",
        help_text="The official name or number of the train (e.g., 'IC 123 Kyiv Express').",
    )
    cargo_num = models.IntegerField(
        verbose_name="Number of cargos",
        help_text="Total number of cargo (carriages/compartments) in the train.",
    )
    places_in_cargo = models.IntegerField(
        verbose_name="Seats per cargo",
        help_text="Number of seats in each cargo unit (carriage/compartment).",
    )
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.CASCADE,
        verbose_name="Train type",
        help_text="Type/category of the train (select train type ID).",
    )

    def __str__(self):
        return self.name


class Crew(models.Model):
    """
    Represents a crew member, including their first and last name.
    Crew members can be assigned to multiple journeys.
    """

    first_name = models.CharField(
        max_length=100, verbose_name="First name", help_text="Crew member's first name."
    )
    last_name = models.CharField(
        max_length=100, verbose_name="Last name", help_text="Crew member's last name."
    )
    # Many-to-many relation to Journey is defined in Journey

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    """
    Represents a specific journey (trip) taken by a train on a route
    with departure and arrival times and assigned crew.
    """

    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        verbose_name="Route",
        help_text="Route for the journey (select route ID).",
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        verbose_name="Train",
        help_text="Train assigned to the journey (select train ID).",
    )
    departure_time = models.DateTimeField(
        verbose_name="Departure time",
        help_text="Date and time when the journey starts (ISO 8601 format, e.g., '2025-06-15T08:00:00Z').",
    )
    arrival_time = models.DateTimeField(
        verbose_name="Arrival time",
        help_text="Date and time when the journey ends (ISO 8601 format, e.g., '2025-06-15T16:00:00Z').",
    )
    crew = models.ManyToManyField(
        Crew,
        related_name="journeys",
        verbose_name="Assigned crew",
        help_text="List of crew members assigned to this journey.",
    )

    def __str__(self):
        return f"{self.route} ({self.departure_time:%Y-%m-%d %H:%M})"


class Order(models.Model):
    """
    Represents an order placed by a user, containing one or more tickets.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order creation time",
        help_text="Date and time when the order was created (auto-filled).",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="User",
        help_text="User who placed the order (select user ID).",
    )

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class Ticket(models.Model):
    """
    Represents a ticket for a specific seat in a cargo on a journey,
    linked to a specific order.
    """

    cargo = models.IntegerField(
        verbose_name="Cargo number",
        help_text="The number of the cargo (carriage/compartment) where the seat is located.",
    )
    seat = models.IntegerField(
        verbose_name="Seat number",
        help_text="The seat number within the cargo (carriage/compartment).",
    )
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE,
        verbose_name="Journey",
        help_text="Journey for which this ticket is valid (select journey ID).",
    )
    order = models.ForeignKey(
        Order,
        related_name="tickets",
        on_delete=models.CASCADE,
        verbose_name="Order",
        help_text="Order associated with this ticket (select order ID).",
    )

    def __str__(self):
        return f"Ticket {self.id}: Journey {self.journey}, Cargo {self.cargo}, Seat {self.seat}"
