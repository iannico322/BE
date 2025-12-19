from django.urls import path
from .views import PayrollView

urlpatterns = [
    path('all/', PayrollView.as_view(), name='payroll-list-create'),
    path('<int:pk>/', PayrollView.as_view(), name='payroll-detail'),
]