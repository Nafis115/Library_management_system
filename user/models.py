from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='account')
    account_no=models.IntegerField(unique=True)
    balance=models.DecimalField(default=0,max_digits=8,decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)

