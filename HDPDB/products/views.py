import json, bcrypt, jwt, re, datetime
from django.template import Origin
from unittest import result
from unicodedata import name

from django.http     import JsonResponse, HttpResponse
from json.decoder    import JSONDecodeError
from django.views    import View
from django.conf     import settings
import products
import featured

from products.models import MainCategory, SubCategory, OriginProduct, Product, ProductOption, ProductImage
from featured.models import FeaturedName, FeaturedProducts
from core.decorator  import login_decorator
        

class ProductDetailView(View):
    def get(self, request, origin_product_id):
        

        origin_product = OriginProduct.objects.get(id = origin_product_id)
        product = Product.objects.filter(origin_product_id = origin_product.id)
        #product_image = list(ProductImage.objects.filter(origin_product_id = origin_product.id))



        product_information = {
            'name' : origin_product.name,
            #'imageset' : product_image.url,
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

class MainPageView(View):
    def get(self, request, **kwargs):
        
        
        
        if 'main_category' in kwargs.keys() :
            kwargs_value = kwargs['main_category']
            main_category = MainCategory.objects.get(name = kwargs_value)
            sub_category_id_main_category = SubCategory.objects.filter(main_category_id = main_category.id).values('id')
            
            sub_id = []

            for sub_category_id_list in sub_category_id_main_category:
                sub_id.append(sub_category_id_list['id'])
                

            result = [{
                'name' : main_category_filter.name,
            } for main_category_filter in OriginProduct.objects.filter(sub_category_id__in=sub_id)]

            
            return JsonResponse({"message": result}, status=200)

        if 'featured' in kwargs.keys() :
            kwargs_value = kwargs['featured']
            featured_name = FeaturedName.objects.get(space_name = kwargs_value)
            featured_products_list = FeaturedProducts.objects.filter(featured_id = featured_name.id).values('product_origin_id')
            
            orig_pro_id = []

            for i in featured_products_list:
                orig_pro_id.append(i['product_origin_id'])

            print (orig_pro_id)

            result_featured = [
                {
                    'id' : origin_products.id,
                    'name' : origin_products.name,
                } for origin_products in OriginProduct.objects.filter(id__in = orig_pro_id)
            ]

        
            return JsonResponse({"message": result_featured}, status=200)



        else :
            
            

            product_main_all_list = [
                {
                    'id' : origin_product.id,
                    'name' : origin_product.name,
                    'thumbnail_image_url' : origin_product.thumbnail_image_url,
                    'rate_count' : origin_product.rate_count,
                    'review_count' : origin_product.review_count,
                    'sold_count' : origin_product.sold_count,
                } for origin_product in OriginProduct.objects.all()
            ]
            
            return JsonResponse({"message": product_main_all_list}, status=200)
