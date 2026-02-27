from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        fields = ['__all__']
        read_only_fields = ['id' 'date_joined']

    def get_full_name(self, object):
        """Returns user's full name or usrname if not available"""
        if object.first_name and object.last_name:
            return f"{object.first_name} {object.last_name}"
        elif object.first_name:
            return object.first_name
        else:
            return object.username