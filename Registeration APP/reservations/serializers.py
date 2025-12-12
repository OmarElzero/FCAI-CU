from rest_framework import serializers
from django.utils import timezone
from .models import Location, Reservation, ReservationConflict
from activities.models import Activity

class LocationSerializer(serializers.ModelSerializer):
    """Serializer for locations"""
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'capacity', 'facilities', 
                 'available_for_carnival', 'available_for_creativa', 'is_active']

class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reservations"""
    
    class Meta:
        model = Reservation
        fields = ['activity', 'location', 'start_datetime', 'end_datetime', 
                 'reservation_type', 'expected_attendees', 'purpose', 'special_requirements']
    
    def validate(self, attrs):
        # Check if activity is approved
        activity = attrs.get('activity')
        if activity.status != 'approved':
            raise serializers.ValidationError("Can only make reservations for approved activities.")
        
        # Check if user owns the activity
        request = self.context.get('request')
        if request and activity.submitted_by != request.user:
            raise serializers.ValidationError("You can only make reservations for your own activities.")
        
        # Validate datetime
        start_datetime = attrs.get('start_datetime')
        end_datetime = attrs.get('end_datetime')
        
        if start_datetime >= end_datetime:
            raise serializers.ValidationError("End time must be after start time.")
        
        if start_datetime <= timezone.now():
            raise serializers.ValidationError("Reservation must be in the future.")
        
        # Check location availability for reservation type
        location = attrs.get('location')
        reservation_type = attrs.get('reservation_type')
        
        if reservation_type == 'carnival' and not location.available_for_carnival:
            raise serializers.ValidationError("This location is not available for Thursday Carnival events.")
        
        if reservation_type == 'creativa' and not location.available_for_creativa:
            raise serializers.ValidationError("This location is not available for Creativa events.")
        
        # Check capacity
        expected_attendees = attrs.get('expected_attendees')
        if expected_attendees > location.capacity:
            raise serializers.ValidationError(
                f"Expected attendees ({expected_attendees}) exceeds location capacity ({location.capacity})."
            )
        
        return attrs
    
    def create(self, validated_data):
        validated_data['requested_by'] = self.context['request'].user
        return super().create(validated_data)

class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer for listing reservations"""
    activity_name = serializers.CharField(source='activity.team_name')
    location_name = serializers.CharField(source='location.name')
    requested_by_name = serializers.CharField(source='requested_by.get_full_name')
    
    class Meta:
        model = Reservation
        fields = ['id', 'activity_name', 'location_name', 'requested_by_name', 
                 'start_datetime', 'end_datetime', 'reservation_type', 'status', 
                 'expected_attendees', 'request_date']

class ReservationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for reservations"""
    activity = serializers.StringRelatedField()
    location = LocationSerializer(read_only=True)
    requested_by = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()
    conflicts = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = '__all__'
    
    def get_conflicts(self, obj):
        if obj.status == 'pending':
            conflicts = obj.get_conflicts()
            return [{'id': c.id, 'activity': c.activity.team_name, 
                    'start_time': c.start_datetime, 'end_time': c.end_datetime} 
                   for c in conflicts]
        return []

class ReservationReviewSerializer(serializers.ModelSerializer):
    """Serializer for admin to review reservations"""
    
    class Meta:
        model = Reservation
        fields = ['status', 'admin_notes', 'priority_score']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Status must be either 'approved' or 'rejected'.")
        return value

class ReservationFilterSerializer(serializers.Serializer):
    """Serializer for filtering available slots"""
    date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    location = serializers.IntegerField(required=False)
    reservation_type = serializers.ChoiceField(
        choices=Reservation.RESERVATION_TYPE_CHOICES, 
        required=False
    )

class ConflictResolutionSerializer(serializers.ModelSerializer):
    """Serializer for resolving reservation conflicts"""
    
    class Meta:
        model = ReservationConflict
        fields = ['resolution_status', 'resolution_notes']
    
    def validate_resolution_status(self, value):
        if value not in ['resolved', 'escalated']:
            raise serializers.ValidationError("Resolution status must be 'resolved' or 'escalated'.")
        return value