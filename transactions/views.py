from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils import timezone
from django.db import transaction as db_transaction
from .models import Transaction
from books.models import Book
from .serializers import TransactionSerializer



class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for transactions
    Only read operations for security
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter transactions based on your role
        Regular users see their own trasactions
        Admins see all transactions
        """

        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(user=user)
        
    @action(detail=False, methods=['get'])
    def get_transactions(self, request):
        """
        Custom endpoints for user transactions
        """
        transaction = Transaction.objects.filter(user=request.user)
        self.serializer = self.get_serializer(transaction, many = True)
        return response(Serializer.data)
    
    @action(detail=True, methods=['post'])
    def checkout(self, reques, pk=None):
        """
        Custom endpoit for checking out books: POST /api/transactions/{id}/checkout/
        """
        return Response({"cleerror": "Use /api/books/{id}/checkout instead"})
    
    