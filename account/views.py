from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
import random
import string
from datetime import timedelta


# Creating user token
def createRandomUserToken(size=50, chars=string.ascii_letters + string.digits):
    random_token = ''.join(random.choice(chars) for _ in range(size))
    acc_exist = Account.objects.filter(token=random_token)

    if acc_exist.exists():
        createRandomUserToken(
            size=50, chars=string.ascii_letters + string.digits)
    return random_token


class AccountList(APIView):
    def get(self, request, format=None):
        snippets = Account.objects.all()
        serializer = AccountSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user_login = request.data.get("userLogin", None)

        if username is not None or email is not None or password is not None or user_login is not None:
            # For user registration
            if not user_login:
                account_exists = Account.objects.filter(email=email)

                if account_exists.exists():
                    response_msg = {"error": True, "user_exist": True}
                else:
                    # User random token
                    user_token = createRandomUserToken()

                    # Creating account object
                    account_obj = Account(
                        username=username,
                        email=email,
                        password=make_password(password),
                        token=user_token
                    )
                    account_obj.save()

                    response_msg = {
                        "error": False,
                        "account_created": True,
                        "account_id": account_obj.id,
                        "account_password": account_obj.password,
                        "account_created_at": account_obj.created_at - timedelta(hours=8),
                        "token": account_obj.token
                    }
            # For user login
            else:
                try:
                    account_obj = Account.objects.get(email=email)
                except Account.DoesNotExist:
                    response_msg = {"error": True, "user_exist": False}
                else:
                    # Checking password validation
                    valid_password = check_password(
                        password, account_obj.password)

                    if valid_password:
                        response_msg = {
                            "error": False,
                            "login_success": True,
                            "token": account_obj.token
                        }
                    else:
                        response_msg = {
                            "error": True,
                            "login_success": False
                        }

        return Response(response_msg)


class AccountDetail(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AccountSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        response_msg = {"error": True}

        # print(request.data)
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if username is not None or password is not None:
            try:
                account_obj = Account.objects.get(id=pk)
            except:
                response_msg = {"error": True}
            else:
                account_obj.username = username

                if len(password) > 0:
                    account_obj.password = make_password(password)

                account_obj.save()

                response_msg = {
                    "error": False,
                    "account_updated": True,
                    "updated_password": account_obj.password,
                }

        return Response(response_msg)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
