import json

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from account_management.forms import RegistrationSerializer
from account_management.models import User


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        try:
            data = {}
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.set_password(serializer.validated_data['password'])
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data["message"] = "user registered successfully"
                data["username"] = account.username
                data["token"] = token


            else:
                data = serializer.errors

            return Response(data)
        except IntegrityError as e:
            account = User.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        data = {}
        reqBody = json.loads(request.body)
        username = reqBody['username']
        print(username)
        password = reqBody['password']
        try:

            Account = User.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=Account)[0].key
        print(token)
        if not check_password(password, Account.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
