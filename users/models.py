from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    '''
    Custom user manager for handling user creation and superuser creation
    '''

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active_member', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have super_user active')
        
        return self.create_user(email, username, password, **extra_fields)




class CustomUser(AbstractUser):
    '''
    Custom User model for BookHive
    '''
    date_joined = models.DateField(auto_now_add=True)
    is_active_member = models.BooleanField(default=True)
    phone_number = models.CharField(max_length = 15, blank=True)
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} - {"Active" if self.is_active else "Inactive"}'
    
    class Meta:
        verbose_name = 'Library User'
        verbose_name_plural = 'Library Users'