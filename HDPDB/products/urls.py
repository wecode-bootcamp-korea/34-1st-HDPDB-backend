from django.urls import path
from products.views import ProductDetailView

urlpatterns = [
    path('/detail/<int:origin_product_id>', ProductDetailView.as_view())
]