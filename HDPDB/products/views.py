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


class ProductGroupListView(View):
    def get(self, request, **kwargs):
        # GET :8000/product_groups?main_category_id=1 (Audiophile) O
        # GET :8000/product_groups?featured_id=1
        # GET :8000/product_groups?main_category_id=1&featured_id=1

        main_category_id = int(request.GET.get('main_category_id'))
        featured_id = int(request.GET.get('featured_id'))
        
        product_groups = ProductGroup.objects.all()

        if main_category_id:
            product_groups.filter(sub_category__main_category_id=main_category_id)

        if featured_id:
            product_groups.filter(featuredproducts__featured_id=featured_id)

        results = [{
            'id'                  : product_group.id,
            'name'                : product_group.name,
            'thumbnail_image_url' : product_group.thumbnail_image_url,
            'rate_count'          : product_group.rate_count,
            'review_count'        : product_group.review_count,
            'sold_count'          : product_group.sold_count,
        } for product_group in product_groups]

        return JsonResponse({"results": results}, status=200)


from django.models.db import Q

class ProductGroupListView(View):
    def get(self, request):
        main_category_id = int(request.GET.get('main_category_id'))
        featured_id      = int(request.GET.get('featured_id'))

        q = Q()

        if main_category_id:
            q &= Q(sub_category__main_category_id=main_category_id)

        if featured_id:
            q &= Q(featuredproducts__featured_id=featured_id)

        product_groups = ProductGroup.objects.filter(q)

        results = [{
            'id'                  : product_group.id,
            'name'                : product_group.name,
            'thumbnail_image_url' : product_group.thumbnail_image_url,
            'rate_count'          : product_group.rate_count,
            'review_count'        : product_group.review_count,
            'sold_count'          : product_group.sold_count,
        } for product_group in product_groups]


        return JsonResponse({"results": results}, status=200)
