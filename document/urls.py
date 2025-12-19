from django.urls import path
from .views import DocumentView, DocumentSignView, DocumentUploadView

urlpatterns = [
    path('all/', DocumentView.as_view(), name='document-list-create'),
    path('<int:pk>/', DocumentView.as_view(), name='document-detail-edit'),
    path('<int:pk>/sign/', DocumentSignView.as_view(), name='document-sign'),
    path('<int:pk>/upload/', DocumentUploadView.as_view(), name='document-upload'),
]