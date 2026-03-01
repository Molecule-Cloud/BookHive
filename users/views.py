from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response, Serializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import  UserSerializer, RegisterSerializer
from transactions.serializers import TransactionSerializer
from django.contrib.auth import authenticate


class RegisterView(APIView):
    """
    POST /api/register for creating anew user account
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Account Created Successfully",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    """
    POST ap/login - Returns JWT tokens when successful
    """
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "error": "Please enter valid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)

        if not user:
            return Response({
                "error": "Invalid Credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })



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
    

class LogoutView(APIView):
    """POST /api/logout/ - BlackLists the refesh token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "messahe": "Logged out Successfully"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "error": "Invaid Token"
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT /api/profile/ - View and update current user's profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
        