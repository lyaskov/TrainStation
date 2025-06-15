from rest_framework import viewsets, permissions, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from .models import Station, Route, TrainType, Train, Crew, Journey, Order, Ticket
from .permissions import IsAdminOrReadOnly
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
    JourneyCreateSerializer,
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
    permission_classes = [permissions.IsAdminUser]

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
    permission_classes = [permissions.IsAdminUser]


class TrainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows trains to be viewed or edited.
    """

    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAdminUser]


class CrewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows crew members to be viewed or edited.
    """

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [permissions.IsAdminUser]


class JourneyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows journeys to be viewed or edited.
    """

    queryset = Journey.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return JourneyCreateSerializer
        return JourneySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        route = params.get("route")
        if route:
            queryset = queryset.filter(route_id=route)

        train = params.get("train")
        if train:
            queryset = queryset.filter(train_id=train)

        departure_time = params.get("departure_time")
        if departure_time:
            queryset = queryset.filter(departure_time=departure_time)

        dep_from = params.get("dep_from")
        dep_to = params.get("dep_to")
        if dep_from:
            queryset = queryset.filter(departure_time__gte=dep_from)
        if dep_to:
            queryset = queryset.filter(departure_time__lte=dep_to)

        source = params.get("source")
        if source:
            queryset = queryset.filter(route__source_id=source)

        destination = params.get("destination")
        if destination:
            queryset = queryset.filter(route__destination_id=destination)

        return queryset


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
