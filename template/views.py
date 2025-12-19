from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import  Template
from .serializers import  TemplateSerializer

class TemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            template = get_object_or_404( Template, pk=pk)
            serializer =  TemplateSerializer(template)
            return Response(serializer.data)
        templates =  Template.objects.all().order_by('-created_at')
        serializer =  TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer =  TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        template = get_object_or_404( Template, pk=pk)
        serializer =  TemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        template = get_object_or_404( Template, pk=pk)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)