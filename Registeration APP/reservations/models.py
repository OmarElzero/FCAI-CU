from django.db import models
from django.conf import settings
from activities.models import Activity
from django.core.exceptions import ValidationError

class Location(models.Model):
    """Model for available locations that can be reserved"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.IntegerField(help_text="Maximum capacity")
    facilities = models.TextField(blank=True, help_text="Available facilities (projector, sound system, etc.)")
    
    # Special flags
    available_for_carnival = models.BooleanField(default=True, help_text="Available for Thursday Carnival")
    available_for_creativa = models.BooleanField(default=True, help_text="Available for Creativa events")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    """Model for location/time slot reservations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    RESERVATION_TYPE_CHOICES = [
        ('regular', 'Regular Activity'),
        ('carnival', 'Thursday Carnival'),
        ('creativa', 'Creativa Event'),
    ]
    
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='reservations')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reservations')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_reservations')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reservations')
    
    # Date and time
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    # Reservation details
    reservation_type = models.CharField(max_length=20, choices=RESERVATION_TYPE_CHOICES, default='regular')
    expected_attendees = models.IntegerField(help_text="Expected number of attendees")
    purpose = models.TextField(help_text="Purpose of the reservation")
    special_requirements = models.TextField(blank=True, help_text="Special equipment or setup requirements")
    
    # Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Admin notes about the reservation")
    
    # Priority and conflict resolution
    priority_score = models.IntegerField(default=0, help_text="Priority score for conflict resolution")
    
    request_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.activity.team_name} - {self.location.name} ({self.start_datetime.date()})"
    
    def clean(self):
        """Validate reservation data"""
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("End time must be after start time")
        
        if self.expected_attendees > self.location.capacity:
            raise ValidationError(f"Expected attendees ({self.expected_attendees}) exceeds location capacity ({self.location.capacity})")
        
        # Check special location availability
        if self.reservation_type == 'carnival' and not self.location.available_for_carnival:
            raise ValidationError("This location is not available for Thursday Carnival events")
        
        if self.reservation_type == 'creativa' and not self.location.available_for_creativa:
            raise ValidationError("This location is not available for Creativa events")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def has_conflicts(self):
        """Check if this reservation conflicts with others"""
        conflicts = Reservation.objects.filter(
            location=self.location,
            status='approved',
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(pk=self.pk)
        return conflicts.exists()
    
    def get_conflicts(self):
        """Get conflicting reservations"""
        return Reservation.objects.filter(
            location=self.location,
            status='approved',
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(pk=self.pk)

class ReservationConflict(models.Model):
    """Model to track and resolve reservation conflicts"""
    
    RESOLUTION_STATUS_CHOICES = [
        ('pending', 'Pending Resolution'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated to Super Admin'),
    ]
    
    reservation1 = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='conflicts_as_first')
    reservation2 = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='conflicts_as_second')
    
    resolution_status = models.CharField(max_length=20, choices=RESOLUTION_STATUS_CHOICES, default='pending')
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Conflict: {self.reservation1.activity.team_name} vs {self.reservation2.activity.team_name}"
