from django.urls import path
from .views import BudgetView

urlpatterns = [
    path('all/', BudgetView.as_view(), name='budget-list'),
    path('all/<int:proj_id>/', BudgetView.as_view(), name='budget-list-by-project'),
    path('<int:pk>/', BudgetView.as_view(), name='budget-detail'),
]