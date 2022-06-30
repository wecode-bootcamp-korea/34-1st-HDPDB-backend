from email import message
import json, bcrypt, jwt, re, datetime

from django.http import JsonResponse
from django.shortcuts import render
from requests import request

from django.views    import View
from django.conf     import settings
from order.models    import Cart
from products.models import ProductGroup, ProductOption, Product

from json import JSONDecodeError

from core.decorator  import login_required

class CartView(View):
    @login_required
    def post(self, request):
        
        try:
            data = json.loads(request.body)

            user = request.user
            product_id = data['product_id']
            quantity = data['quantity']

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status=400)

            # if quantity <= 0:
            #     return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            cart, is_created = Cart.objects.get_or_create(
                user = user,
                product_id = product_id,
                quantity = quantity

            )
            # cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    @login_required
    def get(self, request):
        try:
            user = request.user

            if not Cart.objects.filter(user=user).exists():
                return JsonResponse({'message' : 'USER_CART_NOT_EXIST'}, status = 400)

            carts = Cart.objects.filter(user=user)
            
            result = [{
                'cart_id' : cart.id,
                'product_name' : cart.product.product_group.name,
                'price' : cart.product.price if not cart.product.discount_price else cart.product.discount_price
            } for cart in carts]
            return JsonResponse({'result' : result}, status=200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_required
    def patch(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            cart_id = request.GET.get('id')
            quantity = data['quantity']

            if not Cart.objects.filter(user=user).exists():
                return JsonResponse({'message' : 'USER_CART_NOT_EXIST'}, status = 400)

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.quantity = data['quantity']
            cart.save()
            return JsonResponse({'quantity': cart.quantity}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_required
    def delete(self, request):
        try:
            user = request.user
            cart_id = request.GET.get('id')

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.delete()
            return JsonResponse({'message': 'DELETED'}, status=200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

