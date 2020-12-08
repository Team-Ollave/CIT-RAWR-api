import datetime

from django.core import exceptions
from django.db.models import Q
from rest_framework import serializers

from backend.reservations import choices, models
from backend.users.choices import UserType
from backend.users.serializers import UserModelSerializer


class BuildingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = "__all__"


class RoomCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = "__all__"


class RoomImageModelSerializere(serializers.ModelSerializer):
    class Meta:
        model = models.RoomImage
        fields = "__all__"


class RoomModelSerializer(serializers.ModelSerializer):
    room_images = RoomImageModelSerializere(many=True, read_only=True)
    is_generic = serializers.ReadOnlyField()

    class Meta:
        model = models.Room
        fields = "__all__"


class ReservationModelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    event_organizer_name = serializers.SerializerMethodField()
    requestor_data = UserModelSerializer(read_only=True, source="requestor")

    class Meta:
        model = models.Reservation
        exclude = ("date_registered",)
        extra_kwargs = {
            "is_accepted_department": {"default": None},
            "is_accepted_imdc": {"default": None},
            "is_accepted_president": {"default": None},
            "start_time": {
                "format": "%H:%M",
                "input_formats": ("%I:%M %p", "%H:%M"),
            },
            "end_time": {
                "format": "%H:%M",
                "input_formats": ("%I:%M %p", "%H:%M"),
            },
            "event_date": {"input_formats": ("%m-%d-%Y", "%Y-%m-%d")},
        }

    def get_status(self, obj):
        user_type = self.context.get("for_user_type")
        if user_type == UserType.DEPARTMENT:
            if obj.is_accepted_department:
                return choices.ReservationStatus.ACCEPTED
            elif not obj.is_accepted_department:
                return choices.ReservationStatus.DECLINED

            return choices.ReservationStatus.PENDING
        if user_type == UserType.IMDC:
            if obj.is_accepted_department and obj.is_accepted_imdc:
                return choices.ReservationStatus.ACCEPTED
            elif obj.is_accepted_department and not obj.is_accepted_imdc:
                return choices.ReservationStatus.DECLINED

            return choices.ReservationStatus.PENDING
        if user_type == UserType.PRESIDENT:
            if (
                obj.is_accepted_department
                and obj.is_accepted_imdc
                and obj.is_accepted_president
            ):
                return choices.ReservationStatus.ACCEPTED
            if (
                obj.is_accepted_department
                and obj.is_accepted_imdc
                and not obj.is_accepted_department
            ):
                return choices.ReservationStatus.DECLINED

        return obj.status

    def get_event_organizer_name(self, obj):
        try:
            return obj.requestor.profile.display_name
        except Exception:
            return "Anonymous"

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        event_date = attrs.get("event_date")

        if event_date and event_date < datetime.date.today():
            raise exceptions.ValidationError("Date already has passed")

        if (event_date and start_time) and end_time < start_time:
            raise exceptions.ValidationError("start_time must be before end_time.")

        try:
            room = attrs.get("room")
            if room and (
                room.available_start_time > start_time
                or end_time > room.available_end_time
            ):
                raise exceptions.ValidationError("Room is not available in this time.")
        except models.Room.DoesNotExist:
            pass

        if (
            models.Reservation.objects.accepted()
            .filter(event_date=event_date)
            .filter(
                Q(end_time__range=(start_time, end_time))
                | Q(start_time__range=(start_time, end_time))
            )
            .exists()
        ):
            raise exceptions.ValidationError("There's an event in the given time range")

        return attrs


class ReservationQuerySerializer(serializers.Serializer):
    department_id = serializers.IntegerField(required=False)
    for_user_type = serializers.CharField(required=False)
    room = serializers.IntegerField(required=False)

    date = serializers.DateField(required=False)
    upcoming = serializers.BooleanField(required=False)
    today = serializers.BooleanField(required=False, allow_null=True, default=None)
    past = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)
    is_accepted_department = serializers.BooleanField(required=False, allow_null=True)
    is_accepted_imdc = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )
    is_accepted_president = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )

    def validate(self, attrs):
        if (
            status := attrs.get("status")
        ) and status not in choices.ReservationStatus.values:
            raise serializers.ValidationError("status value is invalid.")

        if (user_type := attrs.get("for_user_type")) and user_type not in UserType.values:
            raise serializers.ValidationError("for_user_type value is invalid.")

        return attrs


class RoomsQuerySerializer(serializers.Serializer):
    building_id = serializers.IntegerField(required=False)
    has_reservations = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )


class EarliestAvailabilitySerializer(serializers.Serializer):
    earliest_date = serializers.DateField()
