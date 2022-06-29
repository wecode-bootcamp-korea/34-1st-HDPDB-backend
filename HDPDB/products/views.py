import json, bcrypt, jwt, re, datetime

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.conf      import settings
from django.models.db import Count

from products.models import MainCategory, SubCategory, ProductGroup
from featured.models import FeaturedName, FeaturedProducts
from core.decorator  import login_required
        

class ProductGroupView(View):
    def get(self, request, product_group_id):
        product_group = ProductGroup.objects.annotate(total_review_count = Count('reviews__id')) \
            .prefetch_related('products', 'options') \
            .get(id = product_group_id)

        result = {
            'name'         : product_group.name,
            'images'       : list(product_group.images.values('url')),
            'overview'     : product_group.overview,
            'detail'       : product_group.detail,
            'rate_count'   : product_group.rate_count,
            'review_count' : product_group.total_review_count,
            'products'     : [
                {
                    'id' : product.id,
                    'stock' : product.stock,
                    'price' : product.price,
                    'product_options' : [{
                        'name' : product_option.name,
                        'type' : product_option.type
                        } for product_option in product.options.all()],
                } for product in product_group.products.all()]
        }

        return JsonResponse({"result": result}, status=200)

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
