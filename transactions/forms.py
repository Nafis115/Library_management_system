from django import forms
from .models import Transactions

class TransactionFrom(forms.ModelForm):
    class Meta:
        model=Transactions
        fields=[
            'amount',
        ]
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') 
        super().__init__(*args, **kwargs)  
    
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save() 
    
class DepositForm(TransactionFrom):
    
    def clean_amount(self): 
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') 
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
                )

        return amount
