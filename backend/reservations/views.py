import datetime

from rest_framework import mixins, viewsets

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
    serializer_class = serializers.BuildingModelSerializer


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = models.Room.objects
    serializer_class = serializers.RoomModelSerializer


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = models.Reservation.objects
    serializer_class = serializers.ReservationModelSerializer

    def get_queryset(self):
        serializer = serializers.ReservationQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid():
            return queryset.all()

        if date := serializer.validated_data.get("date"):
            queryset = queryset.filter(event_date=date)

        date_today = datetime.date.today()
        if (today := serializer.validated_data.get("today")) is not None:
            if today:
                queryset = queryset.filter(event_date=date_today)
            elif today is False:
                queryset = queryset.exclude(event_date=date_today)

        if serializer.validated_data.get("upcoming"):
            queryset = queryset.filter(event_date__gte=date_today)

        if serializer.validated_data.get("past"):
            queryset = queryset.filter(event_date__lt=date_today)

        return queryset.all()


class RoomImageViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.RoomImage.objects.all()
    serializer_class = serializers.RoomImageModelSerializere
