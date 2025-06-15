from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Station, Route, TrainType, Train, Crew, Journey, Order, Ticket


class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Station model.
    """

    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    """

    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class RouteShortSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    """

    route_name = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ["route_name", "distance"]

    def get_route_name(self, obj):
        return f"{obj.source.name} - {obj.destination.name}"


class RouteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new routes.
    """

    class Meta:
        model = Route
        fields = ["source", "destination", "distance"]


class TrainTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrainType model.
    """

    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    """
    Serializer for the Train model.
    """

    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = "__all__"


class TrainShortSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying basic train info.
    """

    class Meta:
        model = Train
        fields = ["id", "name"]


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crew model.
    """

    class Meta:
        model = Crew
        fields = "__all__"


class JourneySerializer(serializers.ModelSerializer):
    """
    Serializer for the Journey model.
    """

    route = RouteSerializer(read_only=True)
    train = TrainSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"


class JourneyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Journey model.
    """

    class Meta:
        model = Journey
        fields = ["route", "train", "crew", "departure_time", "arrival_time"]


class TicketJourneySerializer(serializers.ModelSerializer):
    route = RouteShortSerializer(read_only=True)
    train = TrainShortSerializer(read_only=True)

    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]


class OrderTicketSerializer(serializers.ModelSerializer):
    journey_info = TicketJourneySerializer(source="journey", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat", "journey", "journey_info"]


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model.
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

    def get_order_created_at(self, obj):
        if obj.order:
            return obj.order.created_at
        return None


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "tickets", "created_at"]


class NestedTicketSerializer(serializers.ModelSerializer):
    journey = serializers.PrimaryKeyRelatedField(queryset=Journey.objects.all())

    class Meta:
        model = Ticket
        exclude = ["order"]


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = NestedTicketSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

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
