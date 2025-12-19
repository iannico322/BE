from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, proj_id=None):
        if proj_id:
            # Get all expenses for specific project
            expenses = Expense.objects.filter(proj_id=proj_id).order_by('-date')
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        
        if pk:
            # Get single expense
            expense = get_object_or_404(Expense, pk=pk)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        
        # Get all expenses
        expenses = Expense.objects.all().order_by('-date')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)