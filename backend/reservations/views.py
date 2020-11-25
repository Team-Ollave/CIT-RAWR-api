from rest_framework import mixins, viewsets

from .models import Person
from .serializers import PersonModelSerializer


class PersonViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer
