from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pedagog.models.documents import Document
from apps.shared.pagination.custom import CustomPagination
from apps.users.serializers.document import DocumentSerializer


class DocumentView(APIView):
    """
    View for handling document-related operations.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Return the queryset for the user profile.
        """
        return Document.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of documents.
        """
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    """
    View for handling document detail operations.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a specific document by its ID.
        """
        document = get_object_or_404(Document, pk=pk, user=request.user)
        serializer = self.serializer_class(document)
        return Response(serializer.data)

    def delete(self, request, pk=None, *args, **kwargs):
        """
        Delete a specific document by its ID.
        """
        document = get_object_or_404(Document, pk=pk, user=request.user)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None, *args, **kwargs):
        """
        Update a specific document by its ID.
        """
        document = get_object_or_404(Document, pk=pk, user=request.user)
        serializer = self.serializer_class(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
