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

class Featured(TimestampZone):
    event_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'features'

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
    option         = models.CharField(max_length=50)
    stock          = models.IntegerField(default=0)
    price          = models.IntegerField(default=0)

    class Meta:
        db_table = 'products'

class ProductImage(TimestampZone):
    url     = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class FeaturedProducts(models.Model):
    featured       = models.ForeignKey(Featured, on_delete=models.CASCADE)
    product_origin = models.ForeignKey(OriginProduct, on_delete=models.CASCADE)

    class Meta:
        db_table = 'featured_products'

class Discount(TimestampZone):
    activated      = models.BooleanField(default=False)
    name           = models.CharField(max_length=50)
    date_start     = models.DateTimeField(null = True)
    date_end       = models.DateTimeField(null=True)
    percent        = models.IntegerField(null=True)
    discount_price = models.IntegerField(null=True)
        
    class Meta:
        db_table = 'discounts'

class DiscountProduct(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "discount_products"


class Cart(TimestampZone):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
        
    class Meta:
        db_table = 'carts'