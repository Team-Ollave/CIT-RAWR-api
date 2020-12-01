from django.db.models import TextChoices


class Sex(TextChoices):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")


class UserType(TextChoices):
    END_USER = ("E", "End User")
    DEPARTMENT = ("D", "Department")
    IMDC = ("I", "IMDC")
    PRESIDENT = ("P", "President")
