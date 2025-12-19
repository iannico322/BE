from django.urls import path
from .views import QRView

urlpatterns = [
    path('all/', QRView.as_view(), name='qr-list-create'),
    path('<int:pk>/', QRView.as_view(), name='qr-detail'),
]