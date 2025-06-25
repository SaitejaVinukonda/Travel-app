from django.contrib import admin
from .models import Bus, Seat, Tour

class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'bus', 'is_booked']
    list_filter = ['bus', 'is_booked']
    actions = ['reset_seats']

    def reset_seats(self, request, queryset):
        updated = queryset.update(is_booked=False)
        self.message_user(request, f"{updated} seats marked as not booked.")
    reset_seats.short_description = "Reset selected seats (mark as not booked)"

class BusAdmin(admin.ModelAdmin):
    list_display = ['operator', 'source', 'destination', 'departure_time']
    actions = ['reset_all_seats_for_bus']

    def reset_all_seats_for_bus(self, request, queryset):
        total = 0
        for bus in queryset:
            count = Seat.objects.filter(bus=bus).update(is_booked=False)
            total += count
        self.message_user(request, f"{total} seats reset for selected bus(es).")
    reset_all_seats_for_bus.short_description = "Reset all seats for selected buses"

admin.site.register(Bus, BusAdmin)
admin.site.register(Tour)
admin.site.register(Seat, SeatAdmin)