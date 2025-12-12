from django.contrib import admin
from .models import Activity, ActivityTimeline

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'submitted_by', 'status', 'submission_date', 'reviewed_by', 'timeline_published']
    list_filter = ['status', 'submission_date', 'timeline_published']
    search_fields = ['team_name', 'submitted_by__username', 'team_description']
    readonly_fields = ['submission_date', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Team Information', {
            'fields': ('team_name', 'team_description', 'logo', 'previous_contributions', 'expected_contribution')
        }),
        ('Submission Details', {
            'fields': ('submitted_by', 'submission_date')
        }),
        ('Review Information', {
            'fields': ('status', 'reviewed_by', 'review_date', 'admin_notes')
        }),
        ('Timeline', {
            'fields': ('timeline_published', 'timeline_publish_date')
        }),
    ]

@admin.register(ActivityTimeline)
class ActivityTimelineAdmin(admin.ModelAdmin):
    list_display = ['activity', 'published_date', 'featured', 'is_active']
    list_filter = ['published_date', 'featured', 'is_active']
    search_fields = ['activity__team_name']
