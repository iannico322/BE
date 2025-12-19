from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Performer, JudgingCriteria
from .serializers import PerformerSerializer, JudgingCriteriaSerializer

# Create your views here.

class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class JudgingCriteriaViewSet(viewsets.ModelViewSet):
    queryset = JudgingCriteria.objects.all()
    serializer_class = JudgingCriteriaSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class SubmitRatingView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        performer_id = request.data.get('performer_id')
        rater = request.data.get('rater')
        ratings = request.data.get('ratings')
        
        if not performer_id or not rater or not ratings:
            return Response({"error": "performer_id, rater, and ratings are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(ratings, list) or len(ratings) != 5:
            return Response({"error": "ratings must be a list of 5 numbers [Talent, Creativity, Stage Presence, Relevance of ICT, Time Adherence]"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            performer = Performer.objects.get(id=performer_id)
        except Performer.DoesNotExist:
            return Response({"error": "Performer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if this rater already rated this performer
        existing_rating = JudgingCriteria.objects.filter(performer=performer, rater=rater).first()
        if existing_rating:
            return Response({"error": "You have already rated this performer"}, status=status.HTTP_400_BAD_REQUEST)
        
        judging_criteria = JudgingCriteria.objects.create(
            performer=performer,
            rater=rater,
            ratings=ratings
        )
        
        serializer = JudgingCriteriaSerializer(judging_criteria)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PerformerScoresView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request, performer_id):
        try:
            performer = Performer.objects.get(id=performer_id)
        except Performer.DoesNotExist:
            return Response({"error": "Performer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        ratings = JudgingCriteria.objects.filter(performer=performer)
        serializer = JudgingCriteriaSerializer(ratings, many=True)
        
        # Calculate average scores for each criterion
        criteria_names = ["Talent", "Creativity", "Stage Presence", "Relevance of ICT", "Time Adherence"]
        avg_scores = {
            "Talent": 0,
            "Creativity": 0,
            "Stage Presence": 0,
            "Relevance of ICT": 0,
            "Time Adherence": 0,
            "average_total": 0
        }
        
        if ratings.exists():
            count = ratings.count()
            for i in range(5):
                avg_scores[criteria_names[i]] = sum([r.ratings[i] for r in ratings if i < len(r.ratings)]) / count
            avg_scores["average_total"] = sum([r.total_score for r in ratings]) / count
        
        return Response({
            "performer": PerformerSerializer(performer).data,
            "ratings": serializer.data,
            "average_scores": avg_scores
        })

class PerformerRankingView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        performers = Performer.objects.all()
        ranking_data = []
        
        for performer in performers:
            ratings = JudgingCriteria.objects.filter(performer=performer)
            if ratings.exists():
                count = ratings.count()
                avg_total = sum([r.total_score for r in ratings]) / count
                ranking_data.append({
                    "performer": PerformerSerializer(performer).data,
                    "average_total_score": avg_total,
                    "total_ratings": count
                })
        
        # Sort by average total score in descending order
        ranking_data.sort(key=lambda x: x["average_total_score"], reverse=True)
        
        return Response({"ranking": ranking_data})
