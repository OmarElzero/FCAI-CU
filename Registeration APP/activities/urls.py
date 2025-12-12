from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Student endpoints
    path('submit/', views.ActivitySubmissionView.as_view(), name='submit_activity'),
    path('my-activities/', views.StudentActivityListView.as_view(), name='my_activities'),
    
    # Admin endpoints  
    path('admin/list/', views.AdminActivityListView.as_view(), name='admin_activity_list'),
    path('admin/review/<int:pk>/', views.ActivityReviewView.as_view(), name='review_activity'),
    path('admin/stats/', views.activity_stats, name='activity_stats'),
    
    # Common endpoints
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    
    # Public endpoints
    path('timeline/', views.public_timeline, name='public_timeline'),
]