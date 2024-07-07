from django.urls import path
from .views import BooksDetailView,PurchaseHistory,buy_book,return_purchase
urlpatterns = [
  
    path("details/<int:id>", BooksDetailView.as_view(), name="book_details"),
    path('purchase/',PurchaseHistory.as_view(),name="purchase"),
     path('buy/<int:book_id>/', buy_book, name='buy_book'),
     path('return_purchase/<int:purchase_id>/', return_purchase, name='return_purchase'),

]
