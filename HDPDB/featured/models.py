from django.db import models
from products.models import ProductGroup

class Featured(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'featureds'

class FeaturedProducts(models.Model):
    featured      = models.ForeignKey(Featured, on_delete=models.CASCADE, related_name="featured_products")
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="featured_products")

    class Meta:
        db_table = 'featured_products'