from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount
from .constants import GENDER_TYPE

class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email',  'birth_date','gender',  'country', 'city','street_address']
    
    def save(self, commit: True) :
        our_user= super().save(commit=False)
        if commit==True:
            our_user.save()
            UserAccount.objects.create(
                user=our_user,
                account_no=100+our_user.id)
            return our_user
        
       
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

