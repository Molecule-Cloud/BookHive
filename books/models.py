from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
import datetime

class Book(models.Model):
    """
    Book Model: Represents physical books in the library
    """
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    isbn = models.CharField(max_length=13, unique=True, db_index=True, validators=[MinLengthValidator(10), MaxLengthValidator(13)], help_text=f"13-character ISBN of{title}")
    published_date = models.DateField(validators=[MaxValueValidator(datetime.date.today)], help_text="Publication date cannot be in the future")
    total_copies = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    available_copies = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['isbn'])
        ]

    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def is_avaialble(self):
        return self.available_copies > 0
    
    def can_checkout(self):
        return self.is_avaialble()
