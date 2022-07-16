import json
import re

import jwt
import bcrypt
from django.http  import JsonResponse
from django.views import View
from django.conf import settings

from doit.models import User
from my_settings import ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data              = json.loads(request.body)
            user_name         = data['name']
            user_email        = data['email']
            user_password     = data['password']
            user_phone_number = data['phone_number']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', user_email):
                return JsonResponse({'message':'Email format is not valid'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', user_password):
                return JsonResponse({'message':'Password format is not valid'}, status=400)

            if User.objects.filter(email=user_email):
                return JsonResponse({'message':'Email Already Exists'})

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name = user_name,
                email = user_email,
                password = hashed_password,
                phone_number = user_phone_number
            )
            return JsonResponse({'message':'CREATED'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            hashed_password = user.password.encode("utf-8")

            if not bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'id':user.id}, 'secret_key', algorithm=ALGORITHM)

            return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':"JSONDecodeError"}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': "INVALID_USER"}, status=404)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)