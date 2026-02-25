from django.db import models
from django.conf import settings
from books.models import Book
from django.core.validators import MinValueValidator
from datetime import date, timedelta

class Transaction(models.Model):
    """
    Tracks book checkouts and returns one transactiob
    per book copy.
    """
    # === Prevent Invalid statud values
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Checked Out'
        RETURNED = 'RETURNED', 'Returned'
        OVERDUE = 'OVERDUE', 'Overdue'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'transactions',
    )

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='transactions'        
    )

    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, db_index=True)

   
    def save(self, *args, **kwargs):
        """
        Helper function: Overrides save to set due_date if not provides
        Reson: To prevent more bugs
        """
        if not self.due_date:
            self.due_date = date.today() + timedelta(date=14)
        super().save(args, **kwargs)

        def __str__(self):
            return f"{self.user} - {self.book.title} {self.get_status.display()}"

        class Meta:
            ordering = ['-checkout_date']
            indexes = [
                models.Index(fields=['status', 'due_date']),
                models.Index(fields=['user', '-check_out_date'])
                ]