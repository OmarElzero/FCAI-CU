from django.contrib import admin
from .models import Location, Reservation, ReservationConflict

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'available_for_carnival', 'available_for_creativa', 'is_active']
    list_filter = ['available_for_carnival', 'available_for_creativa', 'is_active']
    search_fields = ['name', 'description']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['activity', 'location', 'start_datetime', 'end_datetime', 'status', 'reservation_type']
    list_filter = ['status', 'reservation_type', 'request_date', 'location']
    search_fields = ['activity__team_name', 'location__name', 'requested_by__username']
    
    fieldsets = [
        ('Reservation Details', {
            'fields': ('activity', 'location', 'requested_by', 'reservation_type')
        }),
        ('Date & Time', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Event Details', {
            'fields': ('expected_attendees', 'purpose', 'special_requirements')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'admin_notes', 'priority_score')
        }),
    ]

@admin.register(ReservationConflict)
class ReservationConflictAdmin(admin.ModelAdmin):
    list_display = ['reservation1', 'reservation2', 'resolution_status', 'resolved_by', 'created_at']
    list_filter = ['resolution_status', 'created_at']
    search_fields = ['reservation1__activity__team_name', 'reservation2__activity__team_name']
