from django.urls import path
from .views import ProjectView

urlpatterns = [
    path('all/', ProjectView.as_view(), name='project-list-create'),  # List and create projects
    path('<int:pk>/', ProjectView.as_view(), name='project-retrieve-update-destroy'),  # Retrieve, update, delete specific project
]