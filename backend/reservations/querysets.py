from django.db.models import Q, QuerySet


class ReservationQuerySet(QuerySet):
    def accepted(self):
        return self.filter(
            is_accepted_department=True,
            is_accepted_imdc=True,
            is_accepted_president=True,
        )

    def pending(self):
        return self.filter(
            Q(is_accepted_department=None)
            | Q(is_accepted_imdc=None)
            | Q(is_accepted_president=None)
        )

    def declined(self):
        return self.filter(
            Q(is_accepted_department=False)
            | Q(is_accepted_imdc=False)
            | Q(is_accepted_president=False)
        )

    def from_room(self, room_id):
        return self.filter(room_id=room_id)
