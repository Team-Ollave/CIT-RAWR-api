from rest_framework import mixins, viewsets
from rest_framework.response import Response

from backend.reservations import models, serializers


class BuildingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = models.Building.objects
    serializer_class = serializers.BuildingSerializer


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = models.Room.objects
    serializer_class = serializers.RoomSerializer


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = models.Reservation.objects
    serializer_class = serializers.ReservationSerializer

    def create(self, *args, **kwargs):

        serializer = serializers.CreateReservationRequestSerializers(
            data=self.request.data
        )
        serializer.is_valid(raise_exception=True)

        super().create(*args, **kwargs)

        return Response(serializers.ReservationSerializer(serializer.data).data)
