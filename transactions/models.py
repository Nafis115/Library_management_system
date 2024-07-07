from django.db import models
from user.models import UserAccount

class Transactions(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField(default=0)
    balance_after_transaction = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
