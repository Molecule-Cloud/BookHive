from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet
from transactions.views import TransactionViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'users', UserViewSet, basename='user')

urlpatterns =[
    path('', include(router.urls))
]