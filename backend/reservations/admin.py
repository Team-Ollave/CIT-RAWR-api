from django.contrib import admin

from .models import Building, Notification, Reservation, Room, RoomCategory, RoomImage


admin.site.register(Building)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(Reservation)
admin.site.register(Notification)
