import datetime
from functools import reduce

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.constants import RESERVATION_MAX_HOURS
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

    @action(methods=["GET"], detail=True, url_path="earliest-availability")
    def earliest_availability(self, request, pk):
        try:
            models.Room.objects.get(id=pk)
        except models.Room.DoesNotExist:
            return Response("Room does not exist", status=status.HTTP_400_BAD_REQUEST)

        room_reservations = (
            models.Reservation.objects.from_room(pk)
            .accepted()
            .filter(event_date__gte=datetime.date.today())
            .order_by("event_date", "start_time")
        )

        if room_reservations:
            if room_reservations[0].event_date == datetime.date.today():
                for i in range(len(room_reservations) - 1):
                    if (
                        room_reservations[i].event_date
                        == room_reservations[i + 1].event_date
                    ):
                        event_date = room_reservations[i].event_date
                        if (
                            datetime.datetime.combine(
                                event_date, room_reservations[i + 1].start_time
                            )
                            - datetime.datetime.combine(
                                event_date, room_reservations[i].end_time
                            )
                        ).total_seconds() > RESERVATION_MAX_HOURS:
                            return Response(event_date)
                return Response(
                    room_reservations.last().event_date + datetime.timedelta(days=1)
                )
            else:
                return Response(datetime.date.today())
        else:
            return Response(datetime.date.today())

    @action(methods=["GET"], detail=True, url_path="earliest-availability-v2")
    def earliest_availability_v2(self, request, pk):
        try:
            room = models.Room.objects.get(id=pk)
        except models.Room.DoesNotExist:
            return Response("Room does not exist", status=status.HTTP_400_BAD_REQUEST)
        earliest_availability_date = None
        date_counter = datetime.date.today()
        while not earliest_availability_date:
            room_reservations = (
                models.Reservation.objects.from_room(pk)
                .accepted()
                .filter(event_date=date_counter)
                .order_by("event_date", "start_time")
            )
            if room_reservations:
                total_events_hours = reduce(
                    lambda current, next: current.event_time_length
                    + next.event_time_length,
                    room_reservations,
                )
                if (datetime.today() + total_events_hours) < (
                    datetime.today() + room.max_hours
                ):
                    earliest_availability_date = date_counter
            else:
                earliest_availability_date = date_counter
            date_counter += datetime.timedelta(days=1)
        return Response(earliest_availability_date)


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
            queryset = queryset.from_date(date)

        if user_id := serializer.validated_data.get("user_id"):
            queryset = queryset.from_user(user_id)

        if room := serializer.validated_data.get("room"):
            queryset = queryset.from_room(room)

        if (today := serializer.validated_data.get("today")) is not None:
            queryset = queryset.today(today)

        if serializer.validated_data.get("upcoming"):
            queryset = queryset.upcoming()

        if serializer.validated_data.get("past"):
            queryset = queryset.past()

        if department_id := serializer.validated_data.get("department_id"):
            queryset = queryset.from_department(department_id)

        if status := serializer.validated_data.get("status"):
            for_user_type = serializer.validated_data.get("for_user_type")
            for_user_type = {"for_user": for_user_type} if for_user_type else {}

            if status == choices.ReservationStatus.ACCEPTED:
                queryset = queryset.accepted(**for_user_type)
            elif status == choices.ReservationStatus.DECLINED:
                queryset = queryset.declined(**for_user_type)
            else:
                queryset = queryset.pending(**for_user_type)

        if self.request.query_params.get("is_accepted_department") is not None:
            is_accepted_department = serializer.validated_data.get(
                "is_accepted_department"
            )
            queryset = queryset.accepted_by_department(is_accepted_department)

        if self.request.query_params.get("is_accepted_imdc") is not None:
            is_accepted_imdc = serializer.validated_data.get("is_accepted_imdc")
            queryset = queryset.accepted_by_imdc(is_accepted_imdc)

        if self.request.query_params.get("is_accepted_president") is not None:
            is_accepted_president = serializer.validated_data.get("is_accepted_president")
            queryset = queryset.accepted_by_president(is_accepted_president)

        return queryset.all()

    def get_serializer_context(self):
        query_params = self.request.query_params
        for_user_type = query_params.get("for_user_type")

        context = super().get_serializer_context()
        context.update({"for_user_type": for_user_type})
        return context


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
