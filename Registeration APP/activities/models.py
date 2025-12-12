from django.db import models
from django.conf import settings
from PIL import Image

class Activity(models.Model):
    """Model for student activities"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'rejected'),
        ('meeting_requested', 'Meeting Requested'),
    ]
    
    team_name = models.CharField(max_length=100)
    team_description = models.TextField()
    logo = models.ImageField(upload_to='activity_logos/', null=True, blank=True)
    previous_contributions = models.TextField(help_text="Previous contributions to the faculty")
    expected_contribution = models.TextField(help_text="Expected contribution to the faculty")
    
    # Relationships
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_activities')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_activities')
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Admin notes about the activity")
    
    # Timeline information (populated when approved)
    timeline_published = models.BooleanField(default=False)
    timeline_publish_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.team_name} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize logo if uploaded
        if self.logo:
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path)

class ActivityTimeline(models.Model):
    """Model for published activities timeline"""
    
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, related_name='timeline')
    published_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Additional timeline specific info
    announcement_text = models.TextField(blank=True, help_text="Custom announcement text for timeline")
    featured = models.BooleanField(default=False, help_text="Featured activities appear first")
    
    class Meta:
        ordering = ['-featured', '-published_date']
    
    def __str__(self):
        return f"Timeline: {self.activity.team_name}"
