import datetime

from django.core import exceptions
from rest_framework import serializers

from backend.reservations import models


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = "__all__"


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = "__all__"


class CreateReservationRequestSerializers(serializers.Serializer):
    event_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    event_description = serializers.CharField()
    room = serializers.IntegerField()
    requestor = serializers.IntegerField()

    def validate(self, attrs):
        if attrs["event_date"] < datetime.date.today():
            raise exceptions.ValidationError("Date already has passed")

        if attrs["end_time"] < attrs["start_time"]:
            raise exceptions.ValidationError("Given time invalid")

        room = models.Room.objects.get(id=attrs["room"])
        if (
            room.available_start_time > attrs["start_time"]
            or attrs["end_time"] > room.available_end_time
        ):
            raise exceptions.ValidationError("Room is not available in this time.")

        if models.Reservation.objects.filter(
            event_date=attrs["event_date"],
            start_time__gte=attrs["start_time"],
            end_time__lte=attrs["end_time"],
        ).exists():
            raise exceptions.ValidationError("There's an event in the given time range")

        return attrs
