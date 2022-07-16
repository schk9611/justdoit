import json
import re

import bcrypt
from django.http  import JsonResponse
from django.views import View

from doit.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user_name     = data['name']
            user_email    = data['email']
            user_password = data['password']
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