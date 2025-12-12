from rest_framework import serializers
from .models import Activity, ActivityTimeline

class ActivitySubmissionSerializer(serializers.ModelSerializer):
    """Serializer for activity submission by students"""
    
    class Meta:
        model = Activity
        fields = ['team_name', 'team_description', 'logo', 'previous_contributions', 'expected_contribution']
    
    def create(self, validated_data):
        # Set the submitted_by field to the current user
        validated_data['submitted_by'] = self.context['request'].user
        return super().create(validated_data)

class ActivityListSerializer(serializers.ModelSerializer):
    """Serializer for listing activities (admin view)"""
    submitted_by = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()
    
    class Meta:
        model = Activity
        fields = ['id', 'team_name', 'team_description', 'logo', 'previous_contributions', 
                 'expected_contribution', 'submitted_by', 'status', 'submission_date', 
                 'reviewed_by', 'review_date', 'admin_notes']

class ActivityDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for activity (admin view)"""
    submitted_by = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()
    
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityReviewSerializer(serializers.ModelSerializer):
    """Serializer for admin to review activities"""
    
    class Meta:
        model = Activity
        fields = ['status', 'admin_notes']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected', 'meeting_requested']:
            raise serializers.ValidationError("Invalid status for review.")
        return value

class ActivityTimelineSerializer(serializers.ModelSerializer):
    """Serializer for public timeline"""
    team_name = serializers.CharField(source='activity.team_name')
    team_description = serializers.CharField(source='activity.team_description')
    logo = serializers.ImageField(source='activity.logo')
    submission_date = serializers.DateTimeField(source='activity.submission_date')
    
    class Meta:
        model = ActivityTimeline
        fields = ['id', 'team_name', 'team_description', 'logo', 'submission_date', 
                 'published_date', 'announcement_text', 'featured']