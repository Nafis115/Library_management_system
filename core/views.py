
from django.shortcuts import render, get_object_or_404
from books.models import Books, Category

def home(request, category_slug=None):
    data = Books.objects.all()
    categories = Category.objects.all()  # Rename to plural
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = Books.objects.filter(category=category)
    
    return render(request, 'home.html', {'data': data, 'categories': categories}) 


