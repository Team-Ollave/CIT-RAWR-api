from django.db.models import TextChoices


class Sex(TextChoices):
    MALE = ("M", "Student")
    FEMALE = ("F", "Teacher")
