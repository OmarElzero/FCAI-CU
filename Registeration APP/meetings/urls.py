from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    # Admin endpoints
    path('admin/request/', views.AdminMeetingRequestView.as_view(), name='request_meeting'),
    path('admin/list/', views.AdminMeetingListView.as_view(), name='admin_meeting_list'),
    path('admin/outcome/<int:meeting_id>/', views.update_meeting_outcome, name='update_outcome'),
    path('admin/stats/', views.meeting_stats, name='meeting_stats'),
    
    # Student endpoints
    path('student/list/', views.StudentMeetingListView.as_view(), name='student_meeting_list'),
    path('student/select-slot/<int:meeting_id>/', views.select_time_slot, name='select_time_slot'),
    
    # Common endpoints
    path('<int:pk>/', views.MeetingDetailView.as_view(), name='meeting_detail'),
]