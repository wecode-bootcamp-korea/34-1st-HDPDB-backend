import jwt

from django.db import models
from django.http import JsonResponse

from HDPDB.settings import SECRET_KEY
from users.models import User


class TimestampZone(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
            
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
