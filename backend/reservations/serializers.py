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
