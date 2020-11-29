from django.db.models import Q, QuerySet

from backend.users.choices import UserType


class ReservationQuerySet(QuerySet):
    def accepted(self, for_user: str = UserType.PRESIDENT):
        if for_user in (UserType.DEPARTMENT, UserType.IMDC):
            return self.filter(is_accepted_department=True)

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

    def declined(self):
        return self.filter(
            Q(is_accepted_department=False)
            | Q(is_accepted_imdc=False)
            | Q(is_accepted_president=False)
        )

    def from_department(self, department_id: int):
        return self.filter(room__department_id=department_id)
