import json, bcrypt, jwt, re

from django.http  import JsonResponse
from json.decoder import JSONDecodeError
from django.views import View
from django.conf  import settings
from django.core.exceptions import ValidationError

from users.models import User

class SignUpView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if not re.match(
                '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "ERROR_EMAIL_VALIDATION"}, status=400)

            if len(password) < 8 :
                return JsonResponse({"message": "ERROR_PASSWORD_REQUIRE_8_LETTER"}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message": "ERROR_EMAIL_ALREADY_EXIST"}, status=400)

            name = email[0:email.index('@')]

            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password,
            )
            
            return JsonResponse({"message": "SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)


class SignInView(View):
    def post(self, request):
        
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user = User.objects.get(email = email)

            if not User.objects.filter(email = email).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)         

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    return JsonResponse({"message": "INVALID_USER"}, status=401)

            access_token = jwt.encode({ 'user_id' : user.id }, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({
                "access_token" : access_token
            }, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=401)
