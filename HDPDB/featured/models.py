from django.db import models
from core.utils import TimestampZone
from products.models import OriginProduct

class Featured(TimestampZone):
    event_name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'features'

class FeaturedProducts(models.Model):
    featured       = models.ForeignKey(Featured, on_delete=models.CASCADE)
    product_origin = models.ForeignKey(OriginProduct, on_delete=models.CASCADE)

    class Meta:
        db_table = 'featured_products'