from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Candidate
from .serializers import CandidateSerializer

# Create your views here.

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    http_method_names = ['get', 'post', 'delete']  # Exclude PUT and PATCH
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def list(self, request, *args, **kwargs):
        male_candidates = Candidate.objects.filter(gender='M')
        female_candidates = Candidate.objects.filter(gender='F')
        
        male_serializer = CandidateSerializer(male_candidates, many=True)
        female_serializer = CandidateSerializer(female_candidates, many=True)
        
        return Response({
            "mr": male_serializer.data,
            "ms": female_serializer.data
        })

class UpdateCandidateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def put(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, candidate_id):
        voter_name = request.data.get('voter_name')
        if not voter_name:
            return Response({"error": "voter_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if voter already voted for this specific candidate
        if voter_name in candidate.voters:
            return Response({"error": "You have already voted for this candidate"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if voter already voted for the same gender
        gender_candidates = Candidate.objects.filter(gender=candidate.gender)
        for gc in gender_candidates:
            if voter_name in gc.voters:
                gender_label = "Male" if candidate.gender == 'M' else "Female"
                return Response({"error": f"You have already voted for a {gender_label} candidate"}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate.voters.append(voter_name)
        candidate.votes += 1
        candidate.save()
        
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveVoteView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, candidate_id):
        voter_name = request.data.get('voter_name')
        if not voter_name:
            return Response({"error": "voter_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if voter has voted for this candidate
        if voter_name not in candidate.voters:
            return Response({"error": "You have not voted for this candidate"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove voter from the list
        candidate.voters.remove(voter_name)
        candidate.votes -= 1
        candidate.save()
        
        serializer = CandidateSerializer(candidate)
        return Response({"message": "Vote removed successfully", "candidate": serializer.data}, status=status.HTTP_200_OK)

class RankingView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        male_candidates = Candidate.objects.filter(gender='M').order_by('-votes')
        female_candidates = Candidate.objects.filter(gender='F').order_by('-votes')
        
        male_serializer = CandidateSerializer(male_candidates, many=True)
        female_serializer = CandidateSerializer(female_candidates, many=True)
        
        return Response({
            "mr_ranking": male_serializer.data,
            "ms_ranking": female_serializer.data
        })
