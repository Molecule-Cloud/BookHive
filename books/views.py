from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer



class BookViewSet(viewsets.ModelViewSet):
    """
    Book View for API responses and CRUD Operations
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Custom permission based on actions
        """

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAuthenticated]
        return [self.permission() for permisson in permission_classes]
    

    @action(detail=True, methods = ['post'])
    def checkout(self, requet, pk=None):
        """
        Custo, action for checking out books
        """

        if not Book.is_available():
            return Response(
                {'error': "No copies available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "Happy reading"})