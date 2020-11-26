from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


ROUTER = DefaultRouter()

ROUTER.register("users", UserViewSet)

urlpatterns = path("", include(ROUTER.urls))
