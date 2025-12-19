from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer
from django.utils import timezone

class DocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            document = get_object_or_404(Document, pk=pk)
            serializer = DocumentSerializer(document)
            data = serializer.data
            
            # Add creator details
            if document.created_by:
                creator = document.created_by
                initial_part = f" {creator.inital}. " if creator.inital else " "
                fullname = f"{creator.first_name}{initial_part}{creator.last_name}"
                
                data['created_by'] = {
                    'id': creator.id,
                    'name': fullname,
                    'designation': creator.designation
                }
            
            return Response(data)
            
        documents = Document.objects.all().order_by('-date_created')
        serializer = DocumentSerializer(documents, many=True)
        data = serializer.data
        
        # Add creator details for each document
        for i, document_data in enumerate(data):
            document = documents[i]
            if document.created_by:
                creator = document.created_by
                initial_part = f" {creator.inital}. " if creator.inital else " "
                fullname = f"{creator.first_name}{initial_part}{creator.last_name}"
                
                document_data['created_by'] = {
                    'id': creator.id,
                    'name': fullname,
                    'designation': creator.designation
                }
        
        return Response(data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            # Set created_by to current user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        # Delete uploaded file if it exists
        if document.uploadedFile:
            document.uploadedFile.delete()
        document.delete()
        return Response({"detail": "Document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        # Edit document details (only by creator or staff)
        document = get_object_or_404(Document, pk=pk)
        if not (request.user.is_staff or document.created_by_id == request.user.id):
            return Response({"detail": "You do not have permission to edit this document."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Handle file upload
        if 'uploadedFile' in request.data:
            # If there's an existing file, delete it
            if document.uploadedFile:
                document.uploadedFile.delete()
            # Set isupload to True when file is uploaded
            request.data['isupload'] = True
        
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        
        # Check permissions (only creator or staff can upload)
        if not (request.user.is_staff or document.created_by_id == request.user.id):
            return Response({"detail": "You do not have permission to upload files to this document."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Check if file is provided
        if 'uploadedFile' not in request.FILES:
            return Response({"detail": "No file provided for upload."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Delete existing file if it exists
        if document.uploadedFile:
            document.uploadedFile.delete()
        
        # Upload new file and set isupload to True
        document.uploadedFile = request.FILES['uploadedFile']
        document.isupload = True
        document.save()
        
        serializer = DocumentSerializer(document)
        return Response({
            "detail": "File uploaded successfully.",
            "document": serializer.data
        }, status=status.HTTP_200_OK)

class DocumentSignView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        user_id = request.user.id

        # Check if user is in assignatures
        assignatures = document.assignatures if document.assignatures else []
        found = False
        for signer in assignatures:
            if signer.get('id') == user_id:
                signer['sign_img'] = request.data.get('sign_img', signer.get('sign_img'))
                signer['status'] = True
                signer['signed_date'] = timezone.now().isoformat()
                found = True
                break

        if not found:
            return Response({"detail": "You do not have permission to sign this document."},
                            status=status.HTTP_403_FORBIDDEN)

        document.assignatures = assignatures
        document.save()
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

