from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    availability_status = serializers.SerializerMethodField()

    def get_availability_status(self, object):
        if object.available_copies > 3:
            return f"{object} is available"
        elif object.available_copies <= 3 and object.available_copies != 0:
            return f"{object} is limited"
        else:
            return f"{object} is unavailable"
        
    class Meta:
        model = Book
        fields = ['__all__']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate_isbn(self, value):
        """
        Custom validation for ISBN field
        """
        cleaned = value.replace('-', '').replace(' ', '')
        if len(cleaned) not in [10, 13]:
            raise serializers.ValidationError("ISBN mus be either 10 or 13")
        
        # === Check if it contains only digits for ISBN-13 or digits+X for ISNB-10

        if not (cleaned.isdigit() or (len(cleaned) == 10 and cleaned[:-1].isdigit() and cleaned[-1] in 'xX')):
            raise serializers.ValidationError("Invalid ISBN")
        return cleaned
    
    def validate(self, data):
        """
        Object level validation
        Checks if available copies is more than total copies
        """
        if 'total_copies' in data and 'available_copies' in data:
            if data['available_copies'] > data['total_copies']:
                raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return data