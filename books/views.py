from datetime import timezone

from django.shortcuts import render
from rest_framework import request, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from django.db import transaction as db_transaction

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
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
        Allows authenticated users to borrow books
        """
        book = self.get.object()
        user = request.user

        """
        Checks if:
        - user is authenticated
        - member is active
        - there are availbale copies of the book
        Invalidates user's ability to borrow another book if they already have a pending checkout status
        """

        if user.is_authenticated:
            return Response({
                "error": "Authentication required"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not hasattr(user, 'is_active_member') or not user.is_active_member:
            return Response({
                "Error": "User inactive"
            }, status=status.HTTP_403_FORBIDDEN)

        if not Book.is_available():
            return Response(
                {'error': "No copies available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        active_transaction = Transaction.objects.filter(
            user = user,
            book = book,
            status = "ACTIVE"
        ).exists()

        if active_transaction:
            return Response({"error": "You alreadu have this book checked out"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                transaction = Transaction.objects.create(
                    user=user,
                    book=user,
                    status='ACTIVE'
                )
                book.available_copies -= 1
                book.save()
                serializer = TransactionSerializer(transaction)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """
        POST /api/books/{id}/return/ for returned books
        """
        book = self.get.object()
        user = request.user

        # Find active transaction for the user and book
        try:
            transaction = Transaction.objects.get(
                user=user,
                book=user,
                status='ACTIVE'
            )
        except Transaction.DoesNotExit:
            return Response({
                "error": "No pending checkout"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                transaction = status = 'RETURNED'
                transaction.return_date = timezone.now()
                transaction.save()

                book.available_copies += 1
                book.save()

                return Response({"mesage": "Book returned Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
