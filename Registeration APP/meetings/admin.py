from django.contrib import admin
from .models import Meeting, MeetingTimeSlot

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['activity', 'admin', 'student', 'status', 'scheduled_datetime', 'outcome']
    list_filter = ['status', 'outcome', 'created_at']
    search_fields = ['activity__team_name', 'admin__username', 'student__username']
    
    fieldsets = [
        ('Meeting Information', {
            'fields': ('activity', 'admin', 'student', 'status')
        }),
        ('Scheduling', {
            'fields': ('scheduled_datetime', 'duration_minutes')
        }),
        ('Google Meet', {
            'fields': ('meet_link', 'meet_id')
        }),
        ('Notes', {
            'fields': ('admin_notes_before', 'admin_notes_after', 'student_notes')
        }),
        ('Outcome', {
            'fields': ('outcome',)
        }),
    ]

@admin.register(MeetingTimeSlot)
class MeetingTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'proposed_datetime', 'is_selected']
    list_filter = ['is_selected', 'created_at']
    search_fields = ['meeting__activity__team_name']
