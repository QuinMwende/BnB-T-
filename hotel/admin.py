from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type', 'status', 'price_per_night', 'current_guest')
    list_filter = ('status', 'room_type')
    search_fields = ('id', 'current_guest')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'payment_method', 'booked_by')
    list_filter = ('payment_method', 'check_in', 'check_out')
    search_fields = ('guest_name', 'room__id')
