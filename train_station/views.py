from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, mixins
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
    API endpoint for managing railway stations.

    - Only admin users can create, update, or delete stations.
    - All stations can be listed and retrieved by admins.
    """

    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List all stations",
        operation_description="Retrieve a list of all available railway stations. Admin access required.",
        responses={200: StationSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all stations."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve station details",
        operation_description="Get detailed information about a single railway station by ID. Admin access required.",
        responses={200: StationSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a station by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new station",
        operation_description="Create a new railway station. Only available to admin users.",
        request_body=StationSerializer,
        responses={201: StationSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new station."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update station",
        operation_description="Update the details of an existing station. Only available to admin users.",
        request_body=StationSerializer,
        responses={200: StationSerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update a station."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update station",
        operation_description="Partially update the details of a station. Only available to admin users.",
        request_body=StationSerializer,
        responses={200: StationSerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update of a station."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete station",
        operation_description="Delete a railway station. Only available to admin users.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a station."""
        return super().destroy(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing train routes between stations.

    - Only admin users can create, update, or delete routes.
    - Admins can list all routes and get detailed info by ID.
    """

    queryset = Route.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RouteCreateSerializer
        return RouteSerializer

    @swagger_auto_schema(
        operation_summary="List all routes",
        operation_description="Retrieve a list of all available train routes. Admin access required.",
        responses={200: RouteSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all routes."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve route details",
        operation_description="Get detailed information about a specific train route by ID. Admin access required.",
        responses={200: RouteSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve route by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new route",
        operation_description="Create a new train route. Only available to admin users.",
        request_body=RouteCreateSerializer,
        responses={201: RouteSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new route."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update route",
        operation_description="Update details of an existing train route. Only available to admin users.",
        request_body=RouteCreateSerializer,
        responses={200: RouteSerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update route."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update route",
        operation_description="Partially update the details of a train route. Only available to admin users.",
        request_body=RouteCreateSerializer,
        responses={200: RouteSerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update of a route."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete route",
        operation_description="Delete a train route. Only available to admin users.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a route."""
        return super().destroy(request, *args, **kwargs)


class TrainTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing train types (categories).

    - Only admin users can create, update, or delete train types.
    - Admins can list all train types and get detailed info by ID.
    """

    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List all train types",
        operation_description="Retrieve a list of all available train types. Admin access required.",
        responses={200: TrainTypeSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all train types."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve train type details",
        operation_description="Get detailed information about a specific train type by ID. Admin access required.",
        responses={200: TrainTypeSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve train type by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new train type",
        operation_description="Create a new train type. Only available to admin users.",
        request_body=TrainTypeSerializer,
        responses={201: TrainTypeSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new train type."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update train type",
        operation_description="Update details of an existing train type. Only available to admin users.",
        request_body=TrainTypeSerializer,
        responses={200: TrainTypeSerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update train type."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update train type",
        operation_description="Partially update a train type. Only available to admin users.",
        request_body=TrainTypeSerializer,
        responses={200: TrainTypeSerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update train type."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete train type",
        operation_description="Delete a train type. Only available to admin users.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete train type."""
        return super().destroy(request, *args, **kwargs)


class TrainViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing trains.

    - Only admin users can create, update, or delete trains.
    - Admins can list all trains and get detailed info by ID.
    """

    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List all trains",
        operation_description="Retrieve a list of all available trains. Admin access required.",
        responses={200: TrainSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all trains."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve train details",
        operation_description="Get detailed information about a specific train by ID. Admin access required.",
        responses={200: TrainSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve train by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new train",
        operation_description="Create a new train. Only available to admin users.",
        request_body=TrainSerializer,
        responses={201: TrainSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new train."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update train",
        operation_description="Update details of an existing train. Only available to admin users.",
        request_body=TrainSerializer,
        responses={200: TrainSerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update train."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update train",
        operation_description="Partially update a train. Only available to admin users.",
        request_body=TrainSerializer,
        responses={200: TrainSerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update train."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete train",
        operation_description="Delete a train. Only available to admin users.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete train."""
        return super().destroy(request, *args, **kwargs)


class CrewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing train crew members.

    - Only admin users can create, update, or delete crew members.
    - Admins can list all crew and get detailed info by ID.
    """

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List all crew members",
        operation_description="Retrieve a list of all crew members. Admin access required.",
        responses={200: CrewSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all crew members."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve crew member details",
        operation_description="Get detailed information about a specific crew member by ID. Admin access required.",
        responses={200: CrewSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve crew member by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new crew member",
        operation_description="Create a new crew member. Only available to admin users.",
        request_body=CrewSerializer,
        responses={201: CrewSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new crew member."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update crew member",
        operation_description="Update details of an existing crew member. Only available to admin users.",
        request_body=CrewSerializer,
        responses={200: CrewSerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update crew member."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update crew member",
        operation_description="Partially update a crew member. Only available to admin users.",
        request_body=CrewSerializer,
        responses={200: CrewSerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update crew member."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete crew member",
        operation_description="Delete a crew member. Only available to admin users.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete crew member."""
        return super().destroy(request, *args, **kwargs)


class JourneyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing train journeys (trips).

    - All authenticated users can view the list of journeys and get details.
    - Only admin users can create, update, or delete journeys.
    - Supports filtering by route, train, departure time, and stations via query params.
    """

    queryset = Journey.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return JourneyCreateSerializer
        return JourneySerializer

    @swagger_auto_schema(
        operation_summary="List all journeys",
        operation_description="""
        Retrieve a list of journeys.  
        Available for all authenticated users.  
        Supports the following filters (query parameters):  
        - `route`: Route ID  
        - `train`: Train ID  
        - `departure_time`: Exact departure datetime  
        - `dep_from`: Departure datetime from  
        - `dep_to`: Departure datetime to  
        - `source`: Departure station ID  
        - `destination`: Arrival station ID
        """,
        manual_parameters=[
            openapi.Parameter(
                "route",
                openapi.IN_QUERY,
                description="Route ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "train",
                openapi.IN_QUERY,
                description="Train ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "departure_time",
                openapi.IN_QUERY,
                description="Exact departure datetime (YYYY-MM-DDTHH:MM:SSZ)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "dep_from",
                openapi.IN_QUERY,
                description="Departure datetime from (YYYY-MM-DD or ISO 8601)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "dep_to",
                openapi.IN_QUERY,
                description="Departure datetime to (YYYY-MM-DD or ISO 8601)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "source",
                openapi.IN_QUERY,
                description="Departure station ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "destination",
                openapi.IN_QUERY,
                description="Arrival station ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: JourneySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List journeys with filtering support."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve journey details",
        operation_description="Get detailed information about a specific journey (trip) by ID. Authenticated access required.",
        responses={200: JourneySerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve journey by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new journey",
        operation_description="Create a new train journey. Only admin users can perform this action.",
        request_body=JourneyCreateSerializer,
        responses={201: JourneySerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new journey."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update journey",
        operation_description="Update details of an existing journey. Only admin users can perform this action.",
        request_body=JourneyCreateSerializer,
        responses={200: JourneySerializer(), 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        """Update a journey."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update journey",
        operation_description="Partially update a journey. Only admin users can perform this action.",
        request_body=JourneyCreateSerializer,
        responses={200: JourneySerializer(), 400: "Validation error"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partial update journey."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete journey",
        operation_description="Delete a journey. Only admin users can perform this action.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a journey."""
        return super().destroy(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_description="""
        Retrieve a list of all journeys.

        Available for all authenticated users.  
        Supports the following filter query parameters:
        - `route`: Route ID (e.g., `?route=3`)
        - `train`: Train ID (e.g., `?train=7`)
        - `departure_time`: Exact departure datetime (e.g., `?departure_time=2025-06-15T08:00:00Z`)
        - `dep_from`: Departure datetime from (e.g., `?dep_from=2025-06-15`)
        - `dep_to`: Departure datetime to (e.g., `?dep_to=2025-06-20`)
        - `source`: Departure station ID (e.g., `?source=1`)
        - `destination`: Arrival station ID (e.g., `?destination=2`)
        """,
        manual_parameters=[
            openapi.Parameter(
                "route",
                openapi.IN_QUERY,
                description="Route ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "train",
                openapi.IN_QUERY,
                description="Train ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "departure_time",
                openapi.IN_QUERY,
                description="Exact departure datetime (YYYY-MM-DDTHH:MM:SSZ)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "dep_from",
                openapi.IN_QUERY,
                description="Departure date/time from (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "dep_to",
                openapi.IN_QUERY,
                description="Departure date/time to (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "source",
                openapi.IN_QUERY,
                description="Departure station ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "destination",
                openapi.IN_QUERY,
                description="Arrival station ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of journeys with filtering support.
        """
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint for managing user orders and tickets.

    - Authenticated users can view and create their own orders (with tickets).
    - Each order can contain one or more tickets.
    """

    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all orders for the authenticated user",
        operation_description="Retrieve a list of all orders made by the authenticated user, with ticket details.",
        responses={200: OrderSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all orders for the authenticated user."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve order details",
        operation_description="Get detailed information about a specific order belonging to the authenticated user.",
        responses={200: OrderSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve order details."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new order (with tickets)",
        operation_description="""
        Create a new order with one or more tickets.

        Example request:
        {
            "tickets": [
                {"journey": 10, "cargo": 2, "seat": 10},
                {"journey": 11, "cargo": 1, "seat": 12}
            ]
        }
        """,
        request_body=OrderCreateSerializer,
        responses={201: OrderSerializer(), 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new order with one or more tickets."""
        return super().create(request, *args, **kwargs)


class TicketViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    API endpoint for viewing and deleting user tickets.

    - Authenticated users can list and retrieve their own tickets.
    - Deletion of tickets is allowed (cancelling).
    - Tickets are created only as part of an order (see OrderViewSet).
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Ticket.objects.none()
        return Ticket.objects.filter(order__user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all tickets for the authenticated user",
        operation_description="Retrieve a list of all tickets belonging to the authenticated user.",
        responses={200: TicketSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List all tickets for the authenticated user."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve ticket details",
        operation_description="Get detailed information about a specific ticket belonging to the authenticated user.",
        responses={200: TicketSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve ticket details."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete ticket",
        operation_description="Delete (cancel) a ticket belonging to the authenticated user.",
        responses={204: "No content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete ticket."""
        return super().destroy(request, *args, **kwargs)
