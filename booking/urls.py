from django.urls import path
from .views import BookingView

urlpatterns = [
    path('all/', BookingView.as_view(), name='booking-list-create'),  # List all and create booking
    path('<int:pk>/', BookingView.as_view(), name='booking-detail'),  # Retrieve, update, delete booking by ID
]