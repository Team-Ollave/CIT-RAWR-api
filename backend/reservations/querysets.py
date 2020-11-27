from django.db.models import QuerySet


class ReservationQuerySet(QuerySet):
    def accepted(self):
        return self.filter(
            is_accepted_department=True,
            is_accepted_imdc=True,
            is_accepted_president=True,
        )
