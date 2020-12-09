import datetime

from django.db.models import QuerySet

from backend.users.choices import UserType


class ReservationQuerySet(QuerySet):
    def accepted(self, for_user: str = UserType.PRESIDENT):

        if for_user == UserType.DEPARTMENT:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=None,
                is_accepted_president=None,
            )

        if for_user == UserType.IMDC:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=True,
                is_accepted_president=None,
            )

        return self.filter(
            is_accepted_department=True,
            is_accepted_imdc=True,
            is_accepted_president=True,
        )

    def pending(self, for_user: str = UserType.DEPARTMENT):
        if for_user == UserType.IMDC:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=None,
                is_accepted_president=None,
            )

        if for_user == UserType.PRESIDENT:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=True,
                is_accepted_president=None,
            )

        return self.filter(
            is_accepted_department=None,
            is_accepted_imdc=None,
            is_accepted_president=None,
        )

    def declined(self, for_user: str = UserType.DEPARTMENT):
        if for_user == UserType.IMDC:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=False,
                is_accepted_president=None,
            )

        if for_user == UserType.PRESIDENT:
            return self.filter(
                is_accepted_department=True,
                is_accepted_imdc=True,
                is_accepted_president=False,
            )

        return self.filter(
            is_accepted_department=False,
            is_accepted_imdc=None,
            is_accepted_president=None,
        )

    def from_department(self, department_id: int):
        return self.filter(room__department_id=department_id)

    def from_room(self, room_id: int):
        return self.filter(room_id=room_id)

    def from_date(self, date):
        return self.filter(event_date=date)

    def from_user(self, user_id: int):
        return self.filter(requestor_id=user_id)

    def today(self, val: bool):
        return (
            self.filter(event_date=datetime.date.today())
            if val
            else self.exclude(event_date=datetime.date.today())
        )

    def upcoming(self):
        return self.filter(event_date__gte=datetime.date.today())

    def past(self):
        return self.filter(event_date__lt=datetime.date.today())

    def accepted_by_department(self, is_accepted_department: bool):
        return self.filter(is_accepted_department=is_accepted_department)

    def accepted_by_imdc(self, is_accepted_imdc: bool):
        return self.filter(is_accepted_imdc=is_accepted_imdc)

    def accepted_by_president(self, is_accepted_president: bool):
        return self.filter(is_accepted_president=is_accepted_president)
