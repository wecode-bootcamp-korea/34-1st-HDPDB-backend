from django.urls import path
from products.views import ProductDetailView, MainPageView

urlpatterns = [
    path('/detail/<int:origin_product_id>', ProductDetailView.as_view()),
    path('', MainPageView.as_view()),
    path('/featured/<str:featured>', MainPageView.as_view()),
    path('/<str:main_category>', MainPageView.as_view()),
]