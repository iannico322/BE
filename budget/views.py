from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Budget
from .serializers import BudgetSerializer

class BudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, proj_id=None):
        if proj_id:
            # Get all budgets for specific project
            budgets = Budget.objects.filter(proj_id=proj_id).order_by('-created_date')
            serializer = BudgetSerializer(budgets, many=True)
            return Response(serializer.data)
        
        if pk:
            # Get single budget
            budget = get_object_or_404(Budget, pk=pk)
            serializer = BudgetSerializer(budget)
            return Response(serializer.data)
        
        # Get all budgets
        budgets = Budget.objects.all().order_by('-created_date')
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        serializer = BudgetSerializer(budget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)