from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Station, Route, TrainType, Train, Crew, Journey, Order, Ticket


class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Station model.

    Fields:
      - id: Unique identifier of the station (integer, read-only)
      - name: The official name of the railway station (string)
      - latitude: Latitude of the station in decimal degrees (float)
      - longitude: Longitude of the station in decimal degrees (float)

    Example:
    {
        "id": 1,
        "name": "Kyiv",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    """

    class Meta:
        model = Station
        fields = ["id", "name", "latitude", "longitude"]
        extra_kwargs = {
            "name": {
                "help_text": "The official name of the railway station (e.g., 'Kyiv')"
            },
            "latitude": {
                "help_text": "Latitude of the station in decimal degrees (e.g., 50.4501)"
            },
            "longitude": {
                "help_text": "Longitude of the station in decimal degrees (e.g., 30.5234)"
            },
        }


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.

    Fields:
      - id: Unique identifier of the route (integer, read-only)
      - source: Information about the source (departure) station (StationSerializer, read-only)
      - destination: Information about the destination (arrival) station (StationSerializer, read-only)
      - distance: Distance between stations in kilometers (integer)

    Example:
    {
        "id": 5,
        "source": {
            "id": 1,
            "name": "Kyiv",
            "latitude": 50.4501,
            "longitude": 30.5234
        },
        "destination": {
            "id": 2,
            "name": "Lviv",
            "latitude": 49.8397,
            "longitude": 24.0297
        },
        "distance": 486
    }
    """

    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]
        extra_kwargs = {
            "distance": {
                "help_text": "Distance between stations in kilometers (e.g., 486)"
            }
        }


class RouteShortSerializer(serializers.ModelSerializer):
    """
    Short serializer for Route, used to quickly display the route name and distance.

    Fields:
      - route_name: Human-readable route name in format "Source - Destination" (string)
      - distance: Distance between stations in kilometers (integer)

    Example:
    {
        "route_name": "Kyiv - Lviv",
        "distance": 486
    }
    """

    route_name = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ["route_name", "distance"]
        extra_kwargs = {
            "distance": {
                "help_text": "Distance between stations in kilometers (e.g., 486)"
            }
        }

    def get_route_name(self, obj):
        return f"{obj.source.name} - {obj.destination.name}"


class RouteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new route.

    Fields:
      - source: ID of the source (departure) station (integer, required)
      - destination: ID of the destination (arrival) station (integer, required)
      - distance: Distance between stations in kilometers (integer, required)

    Example:
    {
        "source": 1,
        "destination": 2,
        "distance": 486
    }
    """

    class Meta:
        model = Route
        fields = ["source", "destination", "distance"]
        extra_kwargs = {
            "source": {"help_text": "ID of the source (departure) station."},
            "destination": {"help_text": "ID of the destination (arrival) station."},
            "distance": {
                "help_text": "Distance between stations in kilometers (e.g., 486)."
            },
        }


class TrainTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrainType model.

    Fields:
      - id: Unique identifier of the train type (integer, read-only)
      - name: Name of the train type or category (string, e.g., 'Intercity', 'Regional')

    Example:
    {
        "id": 1,
        "name": "Intercity"
    }
    """

    class Meta:
        model = TrainType
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {
                "help_text": "Name of the train type or category (e.g., 'Intercity')."
            }
        }


class TrainSerializer(serializers.ModelSerializer):
    """
    Serializer for the Train model.

    Fields:
      - id: Unique identifier of the train (integer, read-only)
      - name: Name or number of the train (string)
      - cargo_num: Total number of cargos (carriages/compartments) in the train (integer)
      - places_in_cargo: Number of seats in each cargo (integer)
      - train_type: Detailed info about the train type (TrainTypeSerializer, read-only)

    Example:
    {
        "id": 1,
        "name": "IC 123 Kyiv Express",
        "cargo_num": 12,
        "places_in_cargo": 54,
        "train_type": {
            "id": 1,
            "name": "Intercity"
        }
    }
    """

    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]
        extra_kwargs = {
            "name": {
                "help_text": "The official name or number of the train (e.g., 'IC 123 Kyiv Express')."
            },
            "cargo_num": {
                "help_text": "Total number of cargos (carriages/compartments) in the train."
            },
            "places_in_cargo": {
                "help_text": "Number of seats in each cargo (carriage/compartment)."
            },
        }


class TrainShortSerializer(serializers.ModelSerializer):
    """
    Short serializer for Train, used to display basic information.

    Fields:
      - id: Unique identifier of the train (integer, read-only)
      - name: Name or number of the train (string)

    Example:
    {
        "id": 1,
        "name": "IC 123 Kyiv Express"
    }
    """

    class Meta:
        model = Train
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {
                "help_text": "The official name or number of the train (e.g., 'IC 123 Kyiv Express')."
            }
        }


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crew model.

    Fields:
      - id: Unique identifier of the crew member (integer, read-only)
      - first_name: Crew member's first name (string)
      - last_name: Crew member's last name (string)

    Example:
    {
        "id": 1,
        "first_name": "Ivan",
        "last_name": "Shevchenko"
    }
    """

    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]
        extra_kwargs = {
            "first_name": {"help_text": "Crew member's first name."},
            "last_name": {"help_text": "Crew member's last name."},
        }


class JourneySerializer(serializers.ModelSerializer):
    """
    Serializer for the Journey model.

    Fields:
      - id: Unique identifier of the journey (integer, read-only)
      - route: Detailed information about the route (RouteSerializer, read-only)
      - train: Detailed information about the train (TrainSerializer, read-only)
      - departure_time: Departure datetime in ISO 8601 format (string)
      - arrival_time: Arrival datetime in ISO 8601 format (string)
      - crew: List of assigned crew members (CrewSerializer, read-only)

    Example:
    {
        "id": 10,
        "route": {
            "id": 5,
            "source": {...},
            "destination": {...},
            "distance": 486
        },
        "train": {
            "id": 1,
            "name": "IC 123 Kyiv Express",
            "cargo_num": 12,
            "places_in_cargo": 54,
            "train_type": {...}
        },
        "departure_time": "2025-06-15T08:00:00Z",
        "arrival_time": "2025-06-15T16:00:00Z",
        "crew": [
            {"id": 1, "first_name": "Ivan", "last_name": "Shevchenko"},
            {"id": 2, "first_name": "Petro", "last_name": "Koval"}
        ]
    }
    """

    route = RouteSerializer(read_only=True)
    train = TrainSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = [
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
            "crew",
        ]
        extra_kwargs = {
            "departure_time": {
                "help_text": "Departure date and time (ISO 8601, e.g., '2025-06-15T08:00:00Z')."
            },
            "arrival_time": {
                "help_text": "Arrival date and time (ISO 8601, e.g., '2025-06-15T16:00:00Z')."
            },
        }


class JourneyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Journey.

    Fields:
      - route: ID of the route (integer, required)
      - train: ID of the train (integer, required)
      - crew: List of IDs of assigned crew members (array of integers, required)
      - departure_time: Departure datetime (ISO 8601 string, required)
      - arrival_time: Arrival datetime (ISO 8601 string, required)

    Example:
    {
        "route": 5,
        "train": 1,
        "crew": [1, 2],
        "departure_time": "2025-06-15T08:00:00Z",
        "arrival_time": "2025-06-15T16:00:00Z"
    }
    """

    class Meta:
        model = Journey
        fields = ["route", "train", "crew", "departure_time", "arrival_time"]
        extra_kwargs = {
            "route": {"help_text": "ID of the route for this journey."},
            "train": {"help_text": "ID of the train assigned to this journey."},
            "crew": {"help_text": "List of crew member IDs assigned to this journey."},
            "departure_time": {
                "help_text": "Departure date and time (ISO 8601, e.g., '2025-06-15T08:00:00Z')."
            },
            "arrival_time": {
                "help_text": "Arrival date and time (ISO 8601, e.g., '2025-06-15T16:00:00Z')."
            },
        }


class TicketJourneySerializer(serializers.ModelSerializer):
    """
    Short serializer for Journey, used within Ticket context.

    Fields:
      - id: Unique identifier of the journey (integer, read-only)
      - route: Short information about the route (RouteShortSerializer, read-only)
      - train: Short information about the train (TrainShortSerializer, read-only)
      - departure_time: Departure datetime in ISO 8601 format (string)
      - arrival_time: Arrival datetime in ISO 8601 format (string)

    Example:
    {
        "id": 10,
        "route": {
            "route_name": "Kyiv - Lviv",
            "distance": 486
        },
        "train": {
            "id": 1,
            "name": "IC 123 Kyiv Express"
        },
        "departure_time": "2025-06-15T08:00:00Z",
        "arrival_time": "2025-06-15T16:00:00Z"
    }
    """

    route = RouteShortSerializer(read_only=True)
    train = TrainShortSerializer(read_only=True)

    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]
        extra_kwargs = {
            "departure_time": {"help_text": "Departure date and time (ISO 8601)."},
            "arrival_time": {"help_text": "Arrival date and time (ISO 8601)."},
        }


class OrderTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying tickets within an order context.

    Fields:
      - id: Unique identifier of the ticket (integer, read-only)
      - cargo: Cargo (carriage/compartment) number (integer)
      - seat: Seat number within the cargo (integer)
      - journey: ID of the journey (integer)
      - journey_info: Short info about the journey (TicketJourneySerializer, read-only)

    Example:
    {
        "id": 15,
        "cargo": 2,
        "seat": 10,
        "journey": 10,
        "journey_info": {
            "id": 10,
            "route": {"route_name": "Kyiv - Lviv", "distance": 486},
            "train": {"id": 1, "name": "IC 123 Kyiv Express"},
            "departure_time": "2025-06-15T08:00:00Z",
            "arrival_time": "2025-06-15T16:00:00Z"
        }
    }
    """

    journey_info = TicketJourneySerializer(source="journey", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat", "journey", "journey_info"]
        extra_kwargs = {
            "cargo": {"help_text": "Cargo (carriage/compartment) number."},
            "seat": {"help_text": "Seat number within the cargo."},
            "journey": {"help_text": "ID of the journey."},
        }


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model.

    Fields:
      - id: Unique identifier of the ticket (integer, read-only)
      - order_id: Order (booking) this ticket belongs to (integer, read-only)
      - order_created_at: Date and time when the order was created (ISO 8601 string, read-only)
      - cargo: Cargo (carriage/compartment) number (integer)
      - seat: Seat number within the cargo (integer)
      - journey_info: Short info about the journey (TicketJourneySerializer, read-only)

    Example:
    {
        "id": 15,
        "order_id": 23,
        "order_created_at": "2025-06-14T22:34:18Z",
        "cargo": 2,
        "seat": 10,
        "journey_info": {
            "id": 10,
            "route": {"route_name": "Kyiv - Lviv", "distance": 486},
            "train": {"id": 1, "name": "IC 123 Kyiv Express"},
            "departure_time": "2025-06-15T08:00:00Z",
            "arrival_time": "2025-06-15T16:00:00Z"
        }
    }
    """

    journey_info = TicketJourneySerializer(source="journey", read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(source="order", read_only=True)
    order_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "order_id",
            "order_created_at",
            "cargo",
            "seat",
            "journey_info",
        ]
        extra_kwargs = {
            "cargo": {"help_text": "Cargo (carriage/compartment) number."},
            "seat": {"help_text": "Seat number within the cargo."},
        }

    def get_order_created_at(self, obj):
        if obj.order:
            return obj.order.created_at
        return None


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Fields:
      - id: Unique identifier of the order (integer, read-only)
      - tickets: List of tickets included in the order (array of TicketSerializer)
      - created_at: Date and time when the order was created (ISO 8601 string, read-only)

    Example:
    {
        "id": 23,
        "tickets": [
            {
                "id": 15,
                "order_id": 23,
                "order_created_at": "2025-06-14T22:34:18Z",
                "cargo": 2,
                "seat": 10,
                "journey_info": {
                    "id": 10,
                    "route": {"route_name": "Kyiv - Lviv", "distance": 486},
                    "train": {"id": 1, "name": "IC 123 Kyiv Express"},
                    "departure_time": "2025-06-15T08:00:00Z",
                    "arrival_time": "2025-06-15T16:00:00Z"
                }
            }
        ],
        "created_at": "2025-06-14T22:34:18Z"
    }
    """

    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "tickets", "created_at"]
        extra_kwargs = {
            "created_at": {
                "help_text": "Date and time when the order was created (ISO 8601 format)."
            }
        }


class NestedTicketSerializer(serializers.ModelSerializer):
    """
    Nested serializer for Ticket, used for creating tickets inside an order.

    Fields:
      - journey: ID of the journey (integer, required)
      - cargo: Cargo (carriage/compartment) number (integer, required)
      - seat: Seat number within the cargo (integer, required)

    Example:
    {
        "journey": 10,
        "cargo": 2,
        "seat": 10
    }
    """

    journey = serializers.PrimaryKeyRelatedField(queryset=Journey.objects.all())

    class Meta:
        model = Ticket
        exclude = ["order"]
        extra_kwargs = {
            "journey": {"help_text": "ID of the journey for this ticket."},
            "cargo": {"help_text": "Cargo (carriage/compartment) number."},
            "seat": {"help_text": "Seat number within the cargo."},
        }


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an order with one or more tickets.

    Fields:
      - id: Unique identifier of the order (integer, read-only)
      - created_at: Date and time when the order was created (ISO 8601 string, read-only)
      - tickets: List of ticket objects to include in the order (array of NestedTicketSerializer, required)

    Example:
    {
        "tickets": [
            {
                "journey": 10,
                "cargo": 2,
                "seat": 10
            },
            {
                "journey": 11,
                "cargo": 1,
                "seat": 12
            }
        ]
    }
    """

    tickets = NestedTicketSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]
        extra_kwargs = {
            "created_at": {
                "help_text": "Date and time when the order was created (ISO 8601 format)."
            },
        }

    def validate(self, attrs):
        tickets = attrs.get("tickets", [])
        if not tickets:
            raise ValidationError("Order must contain at least one ticket.")
        seats = set()
        for t in tickets:
            key = (
                t["journey"].id if hasattr(t["journey"], "id") else t["journey"],
                t["cargo"],
                t["seat"],
            )
            if key in seats:
                raise ValidationError(
                    f"Duplicate seat in request: journey={key[0]}, cargo={key[1]}, seat={key[2]}"
                )
            seats.add(key)
        for journey, cargo, seat in seats:
            if Ticket.objects.filter(journey=journey, cargo=cargo, seat=seat).exists():
                raise ValidationError(
                    f"Seat already taken: journey={journey}, cargo={cargo}, seat={seat}"
                )
        return attrs

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        user = self.context["request"].user

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
        return order
