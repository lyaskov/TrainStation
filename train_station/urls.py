from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StationViewSet, RouteViewSet, TrainTypeViewSet, TrainViewSet,
    CrewViewSet, JourneyViewSet, OrderViewSet, TicketViewSet
)

app_name = "train_station"

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'train-types', TrainTypeViewSet)
router.register(r'trains', TrainViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'journeys', JourneyViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
