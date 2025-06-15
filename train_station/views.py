from rest_framework import viewsets, permissions, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from .models import Station, Route, TrainType, Train, Crew, Journey, Order, Ticket
from .serializers import (
    StationSerializer,
    RouteSerializer,
    RouteCreateSerializer,
    TrainTypeSerializer,
    TrainSerializer,
    CrewSerializer,
    JourneySerializer,
    OrderSerializer,
    TicketSerializer,
    OrderCreateSerializer,
)


class StationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stations to be viewed or edited.
    """

    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAdminUser]


class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows routes to be viewed or edited.
    """

    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return RouteCreateSerializer
        return RouteSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows train types to be viewed or edited.
    """

    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trains to be viewed or edited.
    """

    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class CrewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows crew members to be viewed or edited.
    """

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows journeys to be viewed or edited.
    """

    queryset = Journey.objects.all()
    serializer_class = JourneySerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows orders to be viewed or edited.
    {
      "tickets": [
            {"cargo": 1, "seat": 10, "journey": 5},
            {"cargo": 2, "seat": 15, "journey": 5}
                ]
    }
    """

    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class TicketViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows tickets to be viewed or edited.
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data["order"]
        if order.user != self.request.user:
            raise PermissionDenied("You can only create tickets for your own orders.")
        serializer.save()
