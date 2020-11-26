from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **other_fields):
        user = self.create_user(email, password, **other_fields)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user
