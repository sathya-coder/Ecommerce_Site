import random
import string
from django.db import models
from datetime import timedelta, datetime
from ..models.User import *



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_ids = models.CharField(max_length=6, unique=True, null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.product_ids:
            # Generate a six-digit ran
            # dom code
            self.product_ids = ''.join(random.choices(string.digits, k=6))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.CharField(max_length=10)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.full_name}"



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    stock_quantity = models.PositiveIntegerField(default=0)

    


class PasswordResetToken(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=datetime.now() + timedelta(hours=1))

class Coupun(models.Model):
    user_id = models.CharField(max_length=50)
    coupun_code = models.CharField(max_length=50)
    percent_with_price = models.CharField(max_length=50)
    expiry_date = models.DateTimeField()

class UsedCoupuns(models.Model):
    coupun_code_id = models.ForeignKey(Coupun, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Register , on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="1")
