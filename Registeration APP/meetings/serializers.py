from rest_framework import serializers
from django.utils import timezone
from .models import Meeting, MeetingTimeSlot
from activities.models import Activity

class MeetingTimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for meeting time slots"""
    
    class Meta:
        model = MeetingTimeSlot
        fields = ['id', 'proposed_datetime', 'is_selected']

class MeetingRequestSerializer(serializers.ModelSerializer):
    """Serializer for requesting a meeting"""
    time_slots = MeetingTimeSlotSerializer(many=True, write_only=True)
    
    class Meta:
        model = Meeting
        fields = ['activity', 'student', 'admin_notes_before', 'time_slots']
    
    def create(self, validated_data):
        time_slots_data = validated_data.pop('time_slots')
        meeting = Meeting.objects.create(**validated_data, admin=self.context['request'].user)
        
        # Create time slots
        for slot_data in time_slots_data:
            MeetingTimeSlot.objects.create(meeting=meeting, **slot_data)
        
        # Update activity status
        meeting.activity.status = 'meeting_requested'
        meeting.activity.save()
        
        return meeting

class MeetingListSerializer(serializers.ModelSerializer):
    """Serializer for listing meetings"""
    activity_name = serializers.CharField(source='activity.team_name')
    admin_name = serializers.CharField(source='admin.get_full_name')
    student_name = serializers.CharField(source='student.get_full_name')
    time_slots = MeetingTimeSlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meeting
        fields = ['id', 'activity_name', 'admin_name', 'student_name', 'status', 
                 'scheduled_datetime', 'meet_link', 'outcome', 'time_slots', 'created_at']

class MeetingDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for meetings"""
    activity = serializers.StringRelatedField()
    admin = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    time_slots = MeetingTimeSlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meeting
        fields = '__all__'

class TimeSlotSelectionSerializer(serializers.Serializer):
    """Serializer for student to select time slot"""
    time_slot_id = serializers.IntegerField()
    student_notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_time_slot_id(self, value):
        try:
            time_slot = MeetingTimeSlot.objects.get(id=value)
            # Check if the time slot belongs to a meeting accessible by the user
            meeting = time_slot.meeting
            if meeting.student != self.context['request'].user:
                raise serializers.ValidationError("You don't have permission to select this time slot.")
            return value
        except MeetingTimeSlot.DoesNotExist:
            raise serializers.ValidationError("Time slot does not exist.")

class MeetingOutcomeSerializer(serializers.ModelSerializer):
    """Serializer for admin to update meeting outcome"""
    
    class Meta:
        model = Meeting
        fields = ['outcome', 'admin_notes_after']
    
    def update(self, instance, validated_data):
        # Update meeting
        meeting = super().update(instance, validated_data)
        
        # Update activity based on outcome
        outcome = validated_data.get('outcome')
        if outcome == 'approved':
            meeting.activity.status = 'approved'
            meeting.activity.timeline_published = True
            meeting.activity.timeline_publish_date = timezone.now()
            
            # Create timeline entry
            from activities.models import ActivityTimeline
            ActivityTimeline.objects.get_or_create(
                activity=meeting.activity,
                defaults={
                    'announcement_text': f"New activity '{meeting.activity.team_name}' has been approved after meeting!",
                    'featured': False
                }
            )
        elif outcome == 'rejected':
            meeting.activity.status = 'rejected'
        elif outcome == 'needs_revision':
            meeting.activity.status = 'pending'
        
        meeting.activity.save()
        meeting.status = 'completed'
        meeting.save()
        
        return meeting