from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PersonViewSet


ROUTER = DefaultRouter()

ROUTER.register("people", PersonViewSet)

urlpatterns = path("", include(ROUTER.urls))
