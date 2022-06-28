import json, bcrypt, jwt, re, datetime
from unittest import result
from unicodedata import name

from django.http     import JsonResponse, HttpResponse
from json.decoder    import JSONDecodeError
from django.views    import View
from django.conf     import settings
import products

from products.models import MainCategory, SubCategory, OriginProduct, Product, ProductOption, ProductImage
from core.decorator      import login_decorator

class ProductDetailView(View):
    def get(self, request, origin_product_id):
        

        origin_product = OriginProduct.objects.get(id = origin_product_id)
        product = Product.objects.filter(origin_product_id = origin_product.id)
        product_image = list(ProductImage.objects.filter(origin_product_id = origin_product.id))
        sub_category = SubCategory.objects.get(id = origin_product.sub_category_id)
        main_category = MainCategory.objects.get(id = sub_category.main_category_id)

        product_information = {
            'name' : origin_product.name,
            'imageset' : product_image.url,
            'overview' : origin_product.overview,
            'detail' : origin_product.detail,
            'rate_count' : origin_product.rate_count,
            'review_count' : origin_product.review_count,
            'product_info' : [
                {
                    'product_id' : product_info.id,
                    'stock' : product_info.stock,
                    'price' : product_info.price,
                    'product_option' : [{
                        'name' : product_option.name,
                        'type' : product_option.type
                        } for product_option in ProductOption.objects.filter(product_id = product_info.id)],
                } for product_info in product ]
                
            }
        return JsonResponse({"message": product_information}, status=200)