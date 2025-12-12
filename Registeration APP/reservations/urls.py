from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # Location endpoints
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('available-slots/', views.available_slots, name='available_slots'),
    
    # Student endpoints
    path('create/', views.ReservationCreateView.as_view(), name='create_reservation'),
    path('my-reservations/', views.StudentReservationListView.as_view(), name='my_reservations'),
    
    # Admin endpoints
    path('admin/list/', views.AdminReservationListView.as_view(), name='admin_reservation_list'),
    path('admin/review/<int:pk>/', views.ReservationReviewView.as_view(), name='review_reservation'),
    path('admin/conflicts/', views.reservation_conflicts, name='reservation_conflicts'),
    path('admin/resolve-conflict/<int:conflict_id>/', views.resolve_conflict, name='resolve_conflict'),
    path('admin/stats/', views.reservation_stats, name='reservation_stats'),
    
    # Common endpoints
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
]