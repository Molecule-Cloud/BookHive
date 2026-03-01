from django.utils import timezone 
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db import transaction as db_transaction
from .models import Book
from .serializers import BookSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer




class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if book.available_copies <= 0:
            return Response({'error': "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(user=user, book=book, status='ACTIVE').exists():
            return Response({"error": "You already have this book checked out"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                transaction = Transaction.objects.create(user=user, book=book, status='ACTIVE')
                book.available_copies -= 1
                book.save()
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        try:
            transaction = Transaction.objects.get(user=request.user, book=book, status='ACTIVE')
            with db_transaction.atomic():
                transaction.status = 'RETURNED'
                transaction.return_date = timezone.now()
                transaction.save()
                book.available_copies += 1
                book.save()
                return Response({"message": "Book returned Successfully"}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "No pending checkout"}, status=status.HTTP_400_BAD_REQUEST)
