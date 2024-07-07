from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Books(models.Model):
    title = models.CharField(max_length=120)
    price=models.DecimalField(default=0,max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to='books/media/uploads')
    descriptions=models.TextField()
    quantity=models.PositiveIntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
    
    
class Comment(models.Model):
    
    book=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=120)
    email=models.EmailField()
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"comment by {self.name}"
    
class Purchase(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    book=models.ForeignKey(Books,on_delete=models.CASCADE,null=True,blank=True)
    purchase_date=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    

