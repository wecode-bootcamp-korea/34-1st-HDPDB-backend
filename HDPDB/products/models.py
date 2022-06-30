from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class ProductGroup(models.Model):
    name                = models.CharField(max_length=100, unique=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    thumbnail_image_url = models.CharField(max_length=500)
    overview            = models.TextField(null=True)
    detail              = models.TextField(null=True)
    maker               = models.CharField(max_length=30)
    rate_count          = models.IntegerField(default=0)
    review_count        = models.IntegerField(default=0)
    sold_count          = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_groups'

class Product(models.Model):
    product_group  = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="products")
    stock          = models.IntegerField(default=0)
    price          = models.IntegerField(default=0)
    discount_price = models.IntegerField(null=True)

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name    = models.CharField(max_length=50)
    type    = models.CharField(max_length=50)

    class Meta:
        db_table = 'product_options'

class ProductImage(models.Model):
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="images")
    url     = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_images'
