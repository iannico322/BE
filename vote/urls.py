from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, UpdateCandidateView, VoteView, RemoveVoteView, RankingView

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:pk>/', UpdateCandidateView.as_view(), name='update-candidate'),
    path('vote/<int:candidate_id>/', VoteView.as_view(), name='vote'),
    path('remove-vote/<int:candidate_id>/', RemoveVoteView.as_view(), name='remove-vote'),
    path('ranking/', RankingView.as_view(), name='ranking'),
]