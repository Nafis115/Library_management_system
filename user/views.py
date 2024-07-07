
from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.views.generic import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import UserAccount
# Create your views here.


class RegisterView(FormView):
    template_name='user/register.html'
    form_class=RegisterForm
    success_url=reverse_lazy('login')
    
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request,"Account create successfully")
        return super().form_valid(form)
    
    
class LoginView(LoginView):
    template_name='user/login.html'
    
    def get_success_url(self):
        messages.success(self.request,"Login successfully")
        return reverse_lazy('profile')
@login_required 
def logout_view(request):
    logout(request)
    return redirect('homepage') 
 
@login_required   
def profile(request):
    user_account = UserAccount.objects.filter(user=request.user).first()
    balance = user_account.balance if user_account else 0
    
    context = {
        'user': request.user,
        'balance': balance,
    }
    return render(request, 'user/profile.html', context)

