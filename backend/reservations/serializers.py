import datetime

from django.core import exceptions
from django.db.models import Q
from rest_framework import serializers

from backend.reservations import models


class BuildingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = "__all__"


class RoomCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = "__all__"


class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"


class ReservationModelSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = models.Reservation
        exclude = ("date_registered",)
        extra_kwargs = {
            "is_accepted_department": {"default": None},
            "is_accepted_imdc": {"default": None},
            "is_accepted_president": {"default": None},
        }

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        event_date = attrs.get("event_date")

        if event_date < datetime.date.today():
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
            .filter(
                Q(end_time__range=(start_time, end_time))
                | Q(start_time__range=(start_time, end_time))
            )
            .exists()
        ):
            raise exceptions.ValidationError("There's an event in the given time range")

        return attrs
