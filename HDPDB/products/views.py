import json, bcrypt, jwt, re, datetime

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.conf      import settings

from django.db.models import Q
from numpy import product

from products.models import Category, ProductGroup, Product, ProductOption, ProductImage
from featured.models import Featured, FeaturedProducts
from core.decorator  import login_required


class ProductGroupView(View):
    def get(self, request, product_group_id):
        product_group = ProductGroup.objects.all() \
            .prefetch_related('products', 'products__options', 'products__discounts') \

            .get(id = product_group_id)

        result = {
            'name'         : product_group.name,
            'images'       : list(product_group.images.values('url')),
            'overview'     : product_group.overview,
            'detail'       : product_group.detail,
            'rate_count'   : product_group.rate_count,

            'review_count' : product_group.review_count,

            'products'     : [
                {
                    'id' : product.id,
                    'stock' : product.stock,
                    'price' : product.price,
                    'discount_price' : product.discount_price,
                    'product_options' : [{
                        'id'   : product_option.id,
                        'name' : product_option.name,
                        'type' : product_option.type,
                        } for product_option in product.options.all()],
                } for product in product_group.products.all()]
        } 

        return JsonResponse({"result": result}, status=200)


class ProductGroupListView(View):
        # GET :8000/product_groups?category_id=1
        # GET :8000/product_groups?featured_id=1
        # GET :8000/product_groups?main_category_id=1&featured_id=1
        
    def get(self, request):
        category_id = request.GET.get('category_id')
        featured_id = request.GET.get('featured_id')

        q = Q()

        if category_id:
            q &= Q(category_id=category_id)

        if featured_id:
            q &= Q(featured_products__featured_id=featured_id)

        product_groups = ProductGroup.objects.filter(q) \
            .prefetch_related('products')
        
        results = [{
            'id'                  : product_group.id,
            'name'                : product_group.name,
            'thumbnail_image_url' : product_group.thumbnail_image_url,
            'rate_count'          : product_group.rate_count,
            'review_count'        : product_group.review_count,
            'sold_count'          : product_group.sold_count,
            'price'               : product_group.products.first().price
        } for product_group in product_groups]

        return JsonResponse({"results": results}, status=200)
