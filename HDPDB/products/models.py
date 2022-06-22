
from django.db import models

from users.models import User


class Main_Category(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_categories'

class Sub_Category(models.Model):
    name = models.CharField(max_length=45)
    main_category_id = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'sub_categories'

class Featured(models.Model):
    event_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'features'
    

class Discription(models.Model):
    overview = models.CharField(max_length=350)
    detail = models.TextField()
    image_url_set = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'discriptions'

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True) 
    name = models.CharField(max_length=100, unique=True)
    sub_category_id = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    product_code = models.IntegerField(max_length=10, unique=True)
    thumbnail_image_url = models.URLField(Null = True)
    maker = models.CharField(max_length=30)
    option = models.CharField(max_length=50)
    description = models.ForeignKey(Discription, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

class Featured_Products(models.Model):
    featured_id = models.ForeignKey(Featured, on_delete=models.CASCADE)
    product_code_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'featured_products'

class Discount(models.Model):
    sku = models.ForeignKey(Product, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    date_start = models.DateTimeField(Null = True)
    date_end = models.DateTimeField(Null=True)
    percent = models.IntegerField(Null=True)
    discount_price = models.IntegerField(Null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'discounts'


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    sku = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'carts'
