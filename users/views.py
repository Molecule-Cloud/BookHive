from django.shortcuts import render
from rest_framework import viewsets, status, request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import  UserSerializer
from transactions.serializers import TransactionSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        GET /api/users/{id}/history
        Returns borrowing history for a user
        """
        user = self.get_object()
        if request.user != user and not request.is_staff:
            return Response(
                {"error": "You can only view your own history"},
                status=status.HTTP_403_FORBIDDEN
            )
        transactions = user.transactions.all().order_by('-checked_date')
        self.serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)