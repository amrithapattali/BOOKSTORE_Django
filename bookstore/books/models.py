from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    price = models.FloatField(null=True,blank=True)
    image_url = models.CharField(max_length=2083,blank=True)
    follow_author = models.CharField(max_length=2083, blank=True)
    book_available = models.BooleanField()

    def __str__(self):
        return self.title

class Order(models.Model):
    product = models.ForeignKey(Book,max_length=200,null=True,blank=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

class MyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    bio = models.CharField(max_length=200)
    Favorites = models.ManyToManyField(Book)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    image_url = models.CharField(max_length = 2083, default=False)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class SiteReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True, blank=True)
    review = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(choices=((1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')), null=True, blank=True)

    def __str__(self):
        return self.review