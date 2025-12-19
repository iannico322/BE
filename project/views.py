from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Project
from .serializers import ProjectSerializer
from budget.models import Budget

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(Project, pk=pk)
            # Get total budget amount for this project
            budget_sum = Budget.objects.filter(proj_id=pk).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Serialize project data
            serializer = ProjectSerializer(project)
            data = serializer.data
            # Add project amount and budget sum for total
            data['total_budget'] = float(data['amount']) + float(budget_sum)
            return Response(data)
        
        # Get all projects with their total budgets
        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        data = serializer.data
        
        # Add total budget for each project
        for project in data:
            project_id = project['id']
            budget_sum = Budget.objects.filter(proj_id=project_id).aggregate(Sum('amount'))['amount__sum'] or 0
            project['total_budget'] = float(project['amount']) + float(budget_sum)
        
        return Response(data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)