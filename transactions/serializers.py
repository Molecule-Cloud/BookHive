from rest_framework import serializers
from .models import Transaction
from books.serializers import BookSerializer
# from users.serializers import UserSerializer

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the transaction model
    Includes nested book nd user detail in transaction responses
    """

    book_detail = BookSerializer(source='book', read_only=True)#user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['__all__']
        read_only_fields = ['id', 'checkout_date', 'status']
