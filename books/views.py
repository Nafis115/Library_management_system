from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Books, Purchase
from .forms import CommentForm
from user.models import UserAccount
from django.db import transaction

class BooksDetailView(DetailView):
    model = Books
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object
        
        if 'buy' in request.POST:
            return self.handle_purchase(request, book)
        
        if request.user.is_authenticated and Purchase.objects.filter(user=request.user, book=book).exists():
            form = CommentForm(data=request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.book = book
                new_comment.save()
                messages.success(request, 'Your comment has been added.')
        else:
            messages.error(request, 'You must purchase the book to leave a comment.')
        
        return self.get(request, *args, **kwargs)
    
    def handle_purchase(self, request, book):
        if book.quantity > 0:
            book.quantity -= 1
            book.save()
            Purchase.objects.create(user=request.user, book=book)
            messages.success(request, f'You have successfully purchased {book.title}.')
        else:
            messages.error(request, f'Sorry, {book.title} is out of stock.')
        return redirect('book_details', id=book.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        comments = book.comments.all()
        form = CommentForm()
        
        if self.request.user.is_authenticated and Purchase.objects.filter(user=self.request.user, book=book).exists():
            context['show_comment_form'] = True
            context['form'] = form
        
        context['book'] = book
        context['comments'] = comments
        return context

    
@method_decorator(login_required, name='dispatch')
class PurchaseHistory(ListView):
    model = Purchase
    template_name = 'purchase_history.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)
    
@login_required   
def buy_book(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_account = get_object_or_404(UserAccount, user=request.user)
            
            try:
                with transaction.atomic():
                    book_price = book.price
                    user_balance = user_account.balance
                    
                    if user_balance >= book_price:
                        user_account.balance -= book_price
                        user_account.save()
                        
                        book.quantity -= 1
                        book.save()
                        
                        Purchase.objects.create(user=request.user, book=book)
                        
                        messages.success(request, f'You have successfully purchased {book.title}.')
                        return redirect('book_details', id=book_id)  
                    else:
                        messages.error(request, 'Insufficient balance to purchase this book.')
            except Exception as e:
                messages.error(request, f'Error processing purchase: {e}')
        else:
            messages.error(request, 'You must be logged in to purchase books.')
    
    return redirect('book_details', id=book_id)

@login_required
def return_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if purchase.user != request.user:
        messages.error(request, "You are not authorized to return this purchase.")
        return redirect('purchase')

    with transaction.atomic():
        user_account = UserAccount.objects.get(user=request.user)
        try:
            book_price = purchase.book.price  
            
            user_account.balance += book_price
            user_account.save()

            purchase.book.quantity += 1
            purchase.book.save()

            purchase.delete()
            
            messages.success(request, "Purchase returned successfully. Amount has been credited to your account.")
        except Exception as e:
            messages.error(request, f'Error processing return: {e}')

    return redirect('purchase')
