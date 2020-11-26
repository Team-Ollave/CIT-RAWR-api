from django.db.models import TextChoices


class ReservationStatus(TextChoices):
    ACCEPTED = ("A", "Accepted")
    PENDING = ("P", "Pending")
    DECLINED = ("D", "Declined")
