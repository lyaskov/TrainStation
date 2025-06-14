from rest_framework import serializers
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


class TicketJourneySerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    train = TrainSerializer(read_only=True)

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

    class Meta:
        model = Ticket
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    tickets = OrderTicketSerializer(many=True, source="ticket_set", read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
