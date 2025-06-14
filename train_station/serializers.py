from rest_framework import serializers
from .models import Station, Route, TrainType, Train, Crew, Journey, Order, Ticket


class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Station model.
    """
    class Meta:
        model = Station
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    """
    class Meta:
        model = Route
        fields = '__all__'


class TrainTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrainType model.
    """
    class Meta:
        model = TrainType
        fields = '__all__'


class TrainSerializer(serializers.ModelSerializer):
    """
    Serializer for the Train model.
    """
    class Meta:
        model = Train
        fields = '__all__'


class CrewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crew model.
    """
    class Meta:
        model = Crew
        fields = '__all__'


class JourneySerializer(serializers.ModelSerializer):
    """
    Serializer for the Journey model.
    """
    class Meta:
        model = Journey
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    class Meta:
        model = Order
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model.
    """
    class Meta:
        model = Ticket
        fields = '__all__'
