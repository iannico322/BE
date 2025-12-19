from django.urls import path
from .views import TemplateView

urlpatterns = [
    path('all/', TemplateView.as_view(), name='document-list-create'),
    path('<int:pk>/', TemplateView.as_view(), name='document-detail'),
]