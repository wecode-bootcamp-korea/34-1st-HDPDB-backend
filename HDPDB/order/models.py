from django.db import models

from products.models import Product
from users.models import User 

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity    = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
        
    class Meta:
        db_table = 'carts'