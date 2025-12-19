from django.urls import path
from .views import ExpenseView

urlpatterns = [
    path('all/', ExpenseView.as_view(), name='expense-list-create'),
    path('<int:pk>/', ExpenseView.as_view(), name='expense-detail'),
    path('all/<int:proj_id>/', ExpenseView.as_view(), name='expense-list-by-project'),
]