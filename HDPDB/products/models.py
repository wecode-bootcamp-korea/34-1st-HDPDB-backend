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

class OriginProduct(TimestampZone):
    name                = models.CharField(max_length=100, unique=True)
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    thumbnail_image_url = models.URLField(null = True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    overview            = models.CharField(max_length=350)
    detail              = models.TextField()

    class Meta:
        db_table = 'origin_products'

class Product(TimestampZone):
    origin_product = models.ForeignKey(OriginProduct, on_delete=models.CASCADE)
    sku            = models.CharField(max_length=50, unique=True)
    maker          = models.CharField(max_length=30)
    stock          = models.IntegerField(default=0)
    price          = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    class Meta:
        db_table = 'options'

class ProductImage(TimestampZone):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url     = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_images'

class Discount(TimestampZone):
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