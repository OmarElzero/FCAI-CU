from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
import uuid
from .models import Meeting, MeetingTimeSlot
from .serializers import (
    MeetingRequestSerializer, MeetingListSerializer, MeetingDetailSerializer,
    TimeSlotSelectionSerializer, MeetingOutcomeSerializer
)

class AdminMeetingRequestView(generics.CreateAPIView):
    """Admin endpoint to request a meeting with a student team"""
    serializer_class = MeetingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            raise permissions.PermissionDenied("Admin access required.")
        
        meeting = serializer.save(admin=self.request.user)
        return Response({
            'message': 'Meeting request sent successfully',
            'meeting_id': meeting.id
        }, status=status.HTTP_201_CREATED)

class StudentMeetingListView(generics.ListAPIView):
    """List meetings for the current student"""
    serializer_class = MeetingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_student:
            return Meeting.objects.none()
        
        return Meeting.objects.filter(student=self.request.user).order_by('-created_at')

class AdminMeetingListView(generics.ListAPIView):
    """List meetings for admin"""
    serializer_class = MeetingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            return Meeting.objects.none()
        
        queryset = Meeting.objects.all()
        if self.request.user.is_admin:
            # Regular admins see only their meetings
            queryset = queryset.filter(admin=self.request.user)
        
        return queryset.order_by('-created_at')

class MeetingDetailView(generics.RetrieveAPIView):
    """Detailed view of a meeting"""
    serializer_class = MeetingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Meeting.objects.filter(student=user)
        elif user.is_admin:
            return Meeting.objects.filter(admin=user)
        elif user.is_super_admin:
            return Meeting.objects.all()
        return Meeting.objects.none()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def select_time_slot(request, meeting_id):
    """Student endpoint to select a time slot for meeting"""
    if not request.user.is_student:
        return Response({'error': 'Student access required'}, status=status.HTTP_403_FORBIDDEN)
    
    meeting = get_object_or_404(Meeting, id=meeting_id, student=request.user)
    
    if meeting.status != 'requested':
        return Response({'error': 'Meeting is not in requested status'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = TimeSlotSelectionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        time_slot_id = serializer.validated_data['time_slot_id']
        student_notes = serializer.validated_data.get('student_notes', '')
        
        # Get the time slot
        time_slot = get_object_or_404(MeetingTimeSlot, id=time_slot_id, meeting=meeting)
        
        # Update meeting
        meeting.scheduled_datetime = time_slot.proposed_datetime
        meeting.status = 'scheduled'
        meeting.student_notes = student_notes
        
        # Generate Google Meet link (simplified - in real implementation, use Google Calendar API)
        meeting.meet_id = str(uuid.uuid4())[:8]
        meeting.meet_link = f"https://meet.google.com/{meeting.meet_id}"
        
        meeting.save()
        
        # Mark the selected time slot
        time_slot.is_selected = True
        time_slot.save()
        
        return Response({
            'message': 'Time slot selected successfully',
            'meeting': MeetingDetailSerializer(meeting).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_meeting_outcome(request, meeting_id):
    """Admin endpoint to update meeting outcome"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Check if admin has permission to update this meeting
    if request.user.is_admin and meeting.admin != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if meeting.status != 'scheduled' and meeting.status != 'completed':
        return Response({'error': 'Meeting is not scheduled or completed'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = MeetingOutcomeSerializer(meeting, data=request.data)
    if serializer.is_valid():
        meeting = serializer.save()
        return Response({
            'message': 'Meeting outcome updated successfully',
            'meeting': MeetingDetailSerializer(meeting).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def meeting_stats(request):
    """Statistics about meetings (Admin only)"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    queryset = Meeting.objects.all()
    if request.user.is_admin:
        queryset = queryset.filter(admin=request.user)
    
    stats = {
        'total_meetings': queryset.count(),
        'requested_meetings': queryset.filter(status='requested').count(),
        'scheduled_meetings': queryset.filter(status='scheduled').count(),
        'completed_meetings': queryset.filter(status='completed').count(),
        'cancelled_meetings': queryset.filter(status='cancelled').count(),
        'approved_outcomes': queryset.filter(outcome='approved').count(),
        'rejected_outcomes': queryset.filter(outcome='rejected').count(),
        'needs_revision_outcomes': queryset.filter(outcome='needs_revision').count(),
    }
    
    return Response(stats)
