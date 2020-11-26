from django.contrib import admin

from .models import Building, Reservation, Room, RoomCategory


admin.site.register(Building)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Reservation)
