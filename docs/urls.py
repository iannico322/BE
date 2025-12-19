from django.urls import path
from .views import DocumentView

urlpatterns = [
    path('all/', DocumentView.as_view(), name='document-list-create'),
    path('<int:pk>/', DocumentView.as_view(), name='document-detail-edit'),
]