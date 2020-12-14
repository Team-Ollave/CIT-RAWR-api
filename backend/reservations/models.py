from django.db import models

from backend.constants import DEFAULT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH
from backend.reservations.choices import ReservationStatus
from backend.reservations.querysets import NotificationQuerySet, ReservationQuerySet
from backend.users.models import User


class Building(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)

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

    class Meta:
        ordering = ("-building",)

    @property
    def is_generic(self):
        return self.room_category is not None

    def __str__(self):
        return f"{self.id} - {self.building} - {self.name}"


class RoomImage(models.Model):
    image = models.ImageField(upload_to="images/room/")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "room_images"


class Reservation(models.Model):
    event_name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_registered = models.DateTimeField(auto_now_add=True)

    event_description = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    attendees_count = models.PositiveIntegerField(default=0)

    is_accepted_department = models.BooleanField(null=True, default=None)
    is_accepted_imdc = models.BooleanField(null=True, default=None)
    is_accepted_president = models.BooleanField(null=True, default=None)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ReservationQuerySet.as_manager()

    class Meta:
        default_related_name = "reservations"
        ordering = ("room__building__name", "room__name", "event_date", "start_time")

    def __str__(self):
        return f"{self.id} - {self.event_name} - {self.room.name}"

    @property
    def status(self) -> str:
        if (
            self.is_accepted_department
            and self.is_accepted_imdc
            and self.is_accepted_president
        ):
            return ReservationStatus.ACCEPTED
        elif (
            self.is_accepted_department is False
            or self.is_accepted_imdc is False
            or self.is_accepted_president is False
        ):
            return ReservationStatus.DECLINED

        return ReservationStatus.PENDING

    @property
    def is_accepted(self) -> bool:
        return (
            self.is_accepted_department
            and self.is_accepted_imdc
            and self.is_accepted_president
        )

    @property
    def is_pending(self) -> bool:
        return (
            self.is_accepted_department is None
            or self.is_accepted_imdc is None
            or self.is_accepted_president is None
        )

    @property
    def is_declined(self) -> bool:
        return (
            self.is_accepted_department is False
            or self.is_accepted_imdc is False
            or self.is_accepted_president is False
        )


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey("reservations.Reservation", on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.reservation}"
