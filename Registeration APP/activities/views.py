from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Activity, ActivityTimeline
from .serializers import (
    ActivitySubmissionSerializer, ActivityListSerializer, 
    ActivityDetailSerializer, ActivityReviewSerializer, ActivityTimelineSerializer
)

class ActivitySubmissionView(generics.CreateAPIView):
    """Endpoint for students to submit activity requests"""
    serializer_class = ActivitySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Only students can submit activities
        if not self.request.user.is_student:
            raise permissions.PermissionDenied("Only students can submit activities.")
        
        activity = serializer.save(submitted_by=self.request.user)
        return Response({
            'message': 'Activity submitted successfully',
            'activity_id': activity.id
        }, status=status.HTTP_201_CREATED)

class StudentActivityListView(generics.ListAPIView):
    """List activities submitted by the current student"""
    serializer_class = ActivityListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_student:
            return Activity.objects.filter(submitted_by=self.request.user)
        return Activity.objects.none()

class AdminActivityListView(generics.ListAPIView):
    """List all activities for admin review"""
    serializer_class = ActivityListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            raise permissions.PermissionDenied("Admin access required.")
        
        queryset = Activity.objects.all()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-submission_date')

class ActivityDetailView(generics.RetrieveAPIView):
    """Detailed view of an activity"""
    serializer_class = ActivityDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_student:
            # Students can only view their own activities
            return Activity.objects.filter(submitted_by=self.request.user)
        elif self.request.user.is_admin or self.request.user.is_super_admin:
            # Admins can view all activities
            return Activity.objects.all()
        return Activity.objects.none()

class ActivityReviewView(generics.UpdateAPIView):
    """Admin endpoint to review activities (approve/reject/request meeting)"""
    serializer_class = ActivityReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            raise permissions.PermissionDenied("Admin access required.")
        return Activity.objects.all()
    
    def perform_update(self, serializer):
        activity = self.get_object()
        activity.reviewed_by = self.request.user
        activity.review_date = timezone.now()
        
        # If approved, add to timeline
        if serializer.validated_data.get('status') == 'approved':
            activity.timeline_published = True
            activity.timeline_publish_date = timezone.now()
            
            # Create timeline entry
            ActivityTimeline.objects.get_or_create(
                activity=activity,
                defaults={
                    'announcement_text': f"New activity '{activity.team_name}' has been approved!",
                    'featured': False
                }
            )
        
        serializer.save()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_timeline(request):
    """Public API to fetch approved activities timeline"""
    timelines = ActivityTimeline.objects.filter(is_active=True).order_by('-featured', '-published_date')
    
    # Optional filtering
    limit = request.query_params.get('limit', None)
    if limit:
        try:
            timelines = timelines[:int(limit)]
        except ValueError:
            pass
    
    serializer = ActivityTimelineSerializer(timelines, many=True, context={'request': request})
    return Response({
        'count': timelines.count(),
        'results': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_stats(request):
    """Statistics about activities (Admin only)"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        'total_activities': Activity.objects.count(),
        'pending_activities': Activity.objects.filter(status='pending').count(),
        'approved_activities': Activity.objects.filter(status='approved').count(),
        'rejected_activities': Activity.objects.filter(status='rejected').count(),
        'meeting_requested': Activity.objects.filter(status='meeting_requested').count(),
        'timeline_published': Activity.objects.filter(timeline_published=True).count(),
    }
    
    return Response(stats)
