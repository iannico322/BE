from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import QR
from .serializers import QRSerializer

class QRView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            qr = get_object_or_404(QR, pk=pk)
            serializer = QRSerializer(qr)
            return Response(serializer.data)
        
        qrs = QR.objects.all().order_by('-created_date')
        serializer = QRSerializer(qrs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QRSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        qr = get_object_or_404(QR, pk=pk)
        serializer = QRSerializer(qr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qr = get_object_or_404(QR, pk=pk)
        qr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)