from django.db import models

from backend.constants import DEFAULT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH
from backend.reservations.choices import ReservationStatus
from backend.reservations.querysets import ReservationQuerySet
from backend.users.models import User


class Building(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)

    def __str__(self):
        return f"{self.name}"


class RoomCategory(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    class Meta:
        verbose_name_plural = "Room Categories"

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    name = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    available_start_time = models.TimeField()
    available_end_time = models.TimeField()

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_category = models.ForeignKey(
        RoomCategory, on_delete=models.SET_NULL, blank=True, null=True
    )

    department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_generic(self):
        return self.room_category is not None

    def __str__(self):
        return f"{self.id} - {self.building} - {self.name}"


class Reservation(models.Model):
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_registered = models.DateTimeField(auto_now_add=True)

    event_description = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    attendees_count = models.PositiveIntegerField(default=0)

    is_accepted_department = models.BooleanField(default=False)
    is_accepted_imdc = models.BooleanField(default=False)
    is_accepted_president = models.BooleanField(default=False)
    status = models.CharField(
        max_length=1,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ReservationQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.requestor}"

    def is_accepted(self):
        return (
            self.is_accepted_department
            and self.is_accepted_imdc
            and self.is_accepted_president
        )
