from django.urls import path
from products.views import ProductGroupView, ProductGroupListView

urlpatterns = [
    path('/product/<int:product_group_id>', ProductGroupView.as_view()),
    path('/product_groups', ProductGroupListView.as_view()),
]