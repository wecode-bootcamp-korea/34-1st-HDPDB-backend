from django.db import models
from products.models import OriginProduct

class FeaturedName(models.Model):
    name = models.CharField(max_length=200)
    space_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'featured_names'

class FeaturedProducts(models.Model):
    featured       = models.ForeignKey(FeaturedName, on_delete=models.CASCADE)
    product_origin = models.ForeignKey(OriginProduct, on_delete=models.CASCADE)

    class Meta:
        db_table = 'featured_products'