from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .choices import Sex, UserType
from .managers import UserManager


class UserProfile(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    sex = models.CharField(max_length=1, choices=Sex.choices, null=True, blank=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user_type = models.CharField(
        max_length=1,
        choices=UserType.choices,
        default=UserType.END_USER,
    )

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def is_end_user(self):
        return self.user_type == UserType.END_USER

    def is_department(self):
        return self.user_type == UserType.DEPARTMENT

    def is_imdc(self):
        return self.user_type == UserType.IMDC

    def is_president(self):
        return self.user_type == UserType.PRESIDENT
