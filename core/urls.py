from django.urls import path
from .views import home
urlpatterns = [
    path('',home,name="homepage"),
    path('brand/<slug:category_slug>/', home, name='category_wise_books'),
]
