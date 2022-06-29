from tkinter import CASCADE
from django.db import models

from users.models import User
from core.utils import TimestampZone


class MainCategory(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    name          = models.CharField(max_length=45)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class ProductGroup(models.Model):
    name                = models.CharField(max_length=100, unique=True)
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    thumbnail_image_url = models.URLField(null = True)
    overview            = models.CharField(max_length=350)
    detail              = models.TextField(null=True)
    maker               = models.CharField(max_length=30)
    # rate_count          = models.IntegerField(default=0)
    # review_count        = models.IntegerField(default=0)
    # sold_count          = models.IntegerField(default=0)

    class Meta:
        db_table = 'origin_products'

class Review(models.Model):
    content = models.TextField()
    rating  = models.IntegerField(default=0)
    user    = models.ForeignKey('User')

    class Meta:
        db_table = 'reviews'


class Product(models.Model):
    product_group = models.ForeignKey(OriginProduct, on_delete=models.CASCADE, related_name="products")
    stock          = models.IntegerField(default=0)
    price          = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name    = models.CharField(max_length=50)
    type    = models.CharField(max_length=50)
    stock   = models.IntegerField(default=0)
    price   = models.IntegerField(default=0)
    class Meta:
        db_table = 'product_options'

class ProductImage(models.Model):
    origin_product = models.ForeignKey(OriginProduct, on_delete=models.CASCADE, related_name="images")
    url     = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_images'

class Discount(models.Model):
    activated      = models.BooleanField(default=False)
    name           = models.CharField(max_length=50)
    date_start     = models.DateTimeField(null=True)
    date_end       = models.DateTimeField(null=True)
    percent        = models.IntegerField(null=True)
    discount_price = models.IntegerField(null=True)
        
    class Meta:
        db_table = 'discounts'

class DiscountProduct(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'discount_products'


class Cart(TimestampZone):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
        
    class Meta:
        db_table = 'carts'