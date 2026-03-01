from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id' 'date_joined']

    def get_full_name(self, object):
        """Returns user's full name or usrname if not available"""
        if object.first_name and object.last_name:
            return f"{object.first_name} {object.last_name}"
        elif object.first_name:
            return object.first_name
        else:
            return object.username
        
class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration and authentication"""
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
        style={'input_type': 'password'}
    )
    verify_password = serializers.CharField(
        write_only = True,
        required =  True,
        style= {'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'verify_password']

    def validate(self, attributes):
        """
        Validate if passwords matcch
        """
        if attributes['password'] != attributes['verify_password']:
            raise serializers.ValidationError(
                {"password": "Password fields do not match"}
            )
        return attributes
    

    def create(self, validated_data):
        "Encrypt user creation"

        password = validated_data.pop('password')
        validated_data.pop('verify_password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        user.is_active_member = True
        user.save()
        return user