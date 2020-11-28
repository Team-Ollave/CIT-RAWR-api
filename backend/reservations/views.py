import datetime

from rest_framework import mixins, viewsets

from backend.reservations import choices, models, serializers


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

    def get_queryset(self):
        serializer = serializers.RoomsQuerySerializer(data=self.request.query_params)

        queryset = self.queryset
        if not serializer.is_valid(raise_exception=True):
            return queryset.all()

        if building_id := serializer.validated_data.get("building_id"):
            queryset = queryset.filter(building=building_id)

        if (
            has_reservations := serializer.validated_data.get("has_reservations")
        ) is not None:
            if has_reservations:
                queryset = queryset.exclude(reservations=None)
            else:
                queryset = queryset.filter(reservations=None)

        return queryset.all()


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
        if not serializer.is_valid(raise_exception=True):
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

        if status := serializer.validated_data.get("status"):
            if status == choices.ReservationStatus.ACCEPTED:
                queryset = queryset.accepted()
            elif status == choices.ReservationStatus.DECLINED:
                queryset = queryset.declined()
            else:
                queryset = queryset.pending()

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


class RoomCategoryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.RoomCategory.objects
    serializer_class = serializers.RoomCategoryModelSerializer
