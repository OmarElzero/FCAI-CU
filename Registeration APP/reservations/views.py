from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime, time
from .models import Location, Reservation, ReservationConflict
from .serializers import (
    LocationSerializer, ReservationCreateSerializer, ReservationListSerializer,
    ReservationDetailSerializer, ReservationReviewSerializer, ReservationFilterSerializer,
    ConflictResolutionSerializer
)

class LocationListView(generics.ListAPIView):
    """List all active locations"""
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Location.objects.filter(is_active=True)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by reservation type
        reservation_type = self.request.query_params.get('type', None)
        if reservation_type == 'carnival':
            queryset = queryset.filter(available_for_carnival=True)
        elif reservation_type == 'creativa':
            queryset = queryset.filter(available_for_creativa=True)
        
        return queryset

class ReservationCreateView(generics.CreateAPIView):
    """Create a new reservation"""
    serializer_class = ReservationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if not self.request.user.is_student:
            raise permissions.PermissionDenied("Only students can create reservations.")
        
        reservation = serializer.save()
        
        # Check for conflicts and create conflict records
        conflicts = reservation.get_conflicts()
        if conflicts.exists():
            for conflict in conflicts:
                ReservationConflict.objects.get_or_create(
                    reservation1=reservation,
                    reservation2=conflict,
                    defaults={'resolution_status': 'pending'}
                )
        
        return Response({
            'message': 'Reservation created successfully',
            'reservation_id': reservation.id,
            'has_conflicts': conflicts.exists(),
            'conflicts_count': conflicts.count()
        }, status=status.HTTP_201_CREATED)

class StudentReservationListView(generics.ListAPIView):
    """List reservations for current student"""
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_student:
            return Reservation.objects.none()
        
        return Reservation.objects.filter(
            activity__submitted_by=self.request.user
        ).order_by('-request_date')

class AdminReservationListView(generics.ListAPIView):
    """List all reservations for admin review"""
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            return Reservation.objects.none()
        
        queryset = Reservation.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by reservation type
        type_filter = self.request.query_params.get('type', None)
        if type_filter:
            queryset = queryset.filter(reservation_type=type_filter)
        
        return queryset.order_by('-request_date')

class ReservationDetailView(generics.RetrieveAPIView):
    """Detailed view of a reservation"""
    serializer_class = ReservationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Reservation.objects.filter(activity__submitted_by=user)
        elif user.is_admin or user.is_super_admin:
            return Reservation.objects.all()
        return Reservation.objects.none()

class ReservationReviewView(generics.UpdateAPIView):
    """Admin endpoint to review reservations"""
    serializer_class = ReservationReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not (self.request.user.is_admin or self.request.user.is_super_admin):
            return Reservation.objects.none()
        return Reservation.objects.all()
    
    def perform_update(self, serializer):
        reservation = self.get_object()
        reservation.reviewed_by = self.request.user
        reservation.review_date = timezone.now()
        
        # Handle conflict resolution if approved
        new_status = serializer.validated_data.get('status')
        if new_status == 'approved':
            # Handle any pending conflicts
            conflicts = ReservationConflict.objects.filter(
                Q(reservation1=reservation) | Q(reservation2=reservation),
                resolution_status='pending'
            )
            
            for conflict in conflicts:
                # Simple conflict resolution: priority score or first-come-first-served
                other_reservation = conflict.reservation1 if conflict.reservation2 == reservation else conflict.reservation2
                
                if reservation.priority_score > other_reservation.priority_score:
                    # Current reservation wins
                    other_reservation.status = 'rejected'
                    other_reservation.admin_notes = f"Rejected due to conflict with higher priority reservation {reservation.id}"
                    other_reservation.save()
                elif reservation.priority_score < other_reservation.priority_score:
                    # Other reservation wins
                    reservation.status = 'rejected'
                    reservation.admin_notes = f"Rejected due to conflict with higher priority reservation {other_reservation.id}"
                else:
                    # Same priority - first submitted wins
                    if reservation.request_date < other_reservation.request_date:
                        other_reservation.status = 'rejected'
                        other_reservation.admin_notes = f"Rejected due to conflict - other reservation submitted first"
                        other_reservation.save()
                    else:
                        reservation.status = 'rejected'
                        reservation.admin_notes = f"Rejected due to conflict - other reservation submitted first"
                
                # Mark conflict as resolved
                conflict.resolution_status = 'resolved'
                conflict.resolved_by = self.request.user
                conflict.resolved_at = timezone.now()
                conflict.resolution_notes = "Auto-resolved based on priority and submission time"
                conflict.save()
        
        serializer.save()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def available_slots(request):
    """Get available time slots for a location"""
    serializer = ReservationFilterSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    filters = serializer.validated_data
    date_filter = filters.get('date')
    location_id = filters.get('location')
    reservation_type = filters.get('reservation_type')
    
    if not date_filter or not location_id:
        return Response({'error': 'Date and location are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        location = Location.objects.get(id=location_id, is_active=True)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if location supports the reservation type
    if reservation_type == 'carnival' and not location.available_for_carnival:
        return Response({'error': 'Location not available for carnival events'}, status=status.HTTP_400_BAD_REQUEST)
    
    if reservation_type == 'creativa' and not location.available_for_creativa:
        return Response({'error': 'Location not available for creativa events'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get existing approved reservations for that date and location
    existing_reservations = Reservation.objects.filter(
        location=location,
        status='approved',
        start_datetime__date=date_filter
    ).values('start_datetime', 'end_datetime', 'activity__team_name')
    
    return Response({
        'location': LocationSerializer(location).data,
        'date': date_filter,
        'existing_reservations': list(existing_reservations),
        'available_hours': '8:00 - 18:00 (suggested working hours)',
        'note': 'Check existing reservations to find available time slots'
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def reservation_conflicts(request):
    """Get pending reservation conflicts (Admin only)"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    conflicts = ReservationConflict.objects.filter(resolution_status='pending').select_related(
        'reservation1__activity', 'reservation2__activity', 'reservation1__location'
    )
    
    conflict_data = []
    for conflict in conflicts:
        conflict_data.append({
            'id': conflict.id,
            'reservation1': {
                'id': conflict.reservation1.id,
                'activity': conflict.reservation1.activity.team_name,
                'location': conflict.reservation1.location.name,
                'start_time': conflict.reservation1.start_datetime,
                'end_time': conflict.reservation1.end_datetime,
                'priority_score': conflict.reservation1.priority_score,
                'request_date': conflict.reservation1.request_date
            },
            'reservation2': {
                'id': conflict.reservation2.id,
                'activity': conflict.reservation2.activity.team_name,
                'location': conflict.reservation2.location.name,
                'start_time': conflict.reservation2.start_datetime,
                'end_time': conflict.reservation2.end_datetime,
                'priority_score': conflict.reservation2.priority_score,
                'request_date': conflict.reservation2.request_date
            },
            'created_at': conflict.created_at
        })
    
    return Response({
        'count': len(conflict_data),
        'conflicts': conflict_data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def resolve_conflict(request, conflict_id):
    """Manually resolve a reservation conflict (Admin only)"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    conflict = get_object_or_404(ReservationConflict, id=conflict_id, resolution_status='pending')
    
    serializer = ConflictResolutionSerializer(conflict, data=request.data)
    if serializer.is_valid():
        # Additional data from request
        approved_reservation_id = request.data.get('approved_reservation_id')
        
        if approved_reservation_id:
            if approved_reservation_id == conflict.reservation1.id:
                approved_reservation = conflict.reservation1
                rejected_reservation = conflict.reservation2
            elif approved_reservation_id == conflict.reservation2.id:
                approved_reservation = conflict.reservation2
                rejected_reservation = conflict.reservation1
            else:
                return Response({'error': 'Invalid approved reservation ID'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update reservations
            approved_reservation.status = 'approved'
            approved_reservation.reviewed_by = request.user
            approved_reservation.review_date = timezone.now()
            approved_reservation.save()
            
            rejected_reservation.status = 'rejected'
            rejected_reservation.reviewed_by = request.user
            rejected_reservation.review_date = timezone.now()
            rejected_reservation.admin_notes = f"Rejected due to conflict resolution (Conflict ID: {conflict.id})"
            rejected_reservation.save()
        
        # Update conflict
        conflict.resolved_by = request.user
        conflict.resolved_at = timezone.now()
        conflict = serializer.save()
        
        return Response({
            'message': 'Conflict resolved successfully',
            'conflict': {
                'id': conflict.id,
                'status': conflict.resolution_status,
                'notes': conflict.resolution_notes
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def reservation_stats(request):
    """Reservation statistics (Admin only)"""
    if not (request.user.is_admin or request.user.is_super_admin):
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        'total_reservations': Reservation.objects.count(),
        'pending_reservations': Reservation.objects.filter(status='pending').count(),
        'approved_reservations': Reservation.objects.filter(status='approved').count(),
        'rejected_reservations': Reservation.objects.filter(status='rejected').count(),
        'regular_reservations': Reservation.objects.filter(reservation_type='regular').count(),
        'carnival_reservations': Reservation.objects.filter(reservation_type='carnival').count(),
        'creativa_reservations': Reservation.objects.filter(reservation_type='creativa').count(),
        'pending_conflicts': ReservationConflict.objects.filter(resolution_status='pending').count(),
        'resolved_conflicts': ReservationConflict.objects.filter(resolution_status='resolved').count(),
    }
    
    return Response(stats)
