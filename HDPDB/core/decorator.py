import jwt

from django.http import JsonResponse

from HDPDB.settings import SECRET_KEY
from users.models import User


def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            request.user = User.objects.get(id=payload['user_id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
            
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper