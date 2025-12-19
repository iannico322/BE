from django.urls import path
from .views import ListUsersView, UserDetailView, UserListSimpleView

urlpatterns = [
    path('all/', ListUsersView.as_view(), name='user-list'),
    path('update/<int:id>/', ListUsersView.as_view(), name='user-update'),  # Handles PUT and DELETE
    path('delete/<int:id>/', ListUsersView.as_view(), name='user-delete'),  # Optional: alias for DELETE
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('user-all/', UserListSimpleView.as_view(), name='user-list-simple'),
    # other paths...
]
