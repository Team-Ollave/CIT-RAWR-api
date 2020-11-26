from django.db.models import TextChoices


class Sex(TextChoices):
    MALE = ("M", "Student")
    FEMALE = ("F", "Teacher")


class UserType(TextChoices):
    END_USER = ("E", "End User")
    DEPARTMENT = ("D", "Department")
    IMDC = ("I", "IMDC")
    PRESIDENT = ("P", "President")
