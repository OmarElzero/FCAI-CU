from django.db import models
from django.conf import settings
from activities.models import Activity

class Meeting(models.Model):
    """Model for meetings between admins and student teams"""
    
    STATUS_CHOICES = [
        ('requested', 'Meeting Requested'),
        ('scheduled', 'Meeting Scheduled'),
        ('completed', 'Meeting Completed'),
        ('cancelled', 'Meeting Cancelled'),
    ]
    
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='meetings')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_meetings')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_meetings')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    
    # Meeting scheduling
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=30, help_text="Meeting duration in minutes")
    
    # Google Meet integration
    meet_link = models.URLField(blank=True, help_text="Google Meet link")
    meet_id = models.CharField(max_length=100, blank=True, help_text="Google Meet ID")
    
    # Meeting notes and outcome
    admin_notes_before = models.TextField(blank=True, help_text="Admin notes before meeting")
    admin_notes_after = models.TextField(blank=True, help_text="Admin notes after meeting")
    student_notes = models.TextField(blank=True, help_text="Student notes/questions")
    
    # Meeting outcome
    outcome = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Decision'),
        ('approved', 'Activity Approved'),
        ('rejected', 'Activity Rejected'),
        ('needs_revision', 'Needs Revision'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Meeting: {self.activity.team_name} - {self.get_status_display()}"

class MeetingTimeSlot(models.Model):
    """Available time slots proposed by admin for meetings"""
    
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='time_slots')
    proposed_datetime = models.DateTimeField()
    is_selected = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['proposed_datetime']
    
    def __str__(self):
        return f"Time slot: {self.proposed_datetime} for {self.meeting.activity.team_name}"
