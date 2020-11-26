from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.reservations import views


ROUTER = DefaultRouter()

ROUTER.register("buildings", views.ReservationViewSet)
ROUTER.register("reservations", views.ReservationViewSet)
ROUTER.register("rooms", views.RoomViewSet)

urlpatterns = path("", include(ROUTER.urls))
