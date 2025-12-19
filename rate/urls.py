from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerformerViewSet, 
    JudgingCriteriaViewSet, 
    SubmitRatingView, 
    PerformerScoresView,
    PerformerRankingView
)

router = DefaultRouter()
router.register(r'performers', PerformerViewSet)
router.register(r'ratings', JudgingCriteriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit-rating/', SubmitRatingView.as_view(), name='submit-rating'),
    path('performer-scores/<int:performer_id>/', PerformerScoresView.as_view(), name='performer-scores'),
    path('ranking/', PerformerRankingView.as_view(), name='performer-ranking'),
]
