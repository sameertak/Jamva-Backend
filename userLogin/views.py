import base64

from django.db import transaction
from django.shortcuts import render
from _datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import phoneModel
from decouple import config
import os
from twilio.rest import Client

EXPIRY_TIME = 150


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now()))


class OtpLogin(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, phone, name):
        global user
        try:
            user = phoneModel.objects.get(name=name)
        except ObjectDoesNotExist:
            user = phoneModel.objects.create(
                mobile=phone,
                name=name
            )

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)

        account_sid = config('account_sid')
        auth_token = config('auth_token')
        client = Client(account_sid, auth_token)
        # print(OTP.now())
        client.messages.create(
            body=f"Your OTP is {OTP.now()}",
            from_=config('from_'),
            to=f"+91{phone}"
        )

        return Response(
            status=status.HTTP_200_OK,
            data={
                "id": user.id
            }
        )

    @staticmethod
    def post(request, phone, name):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)
        try:
            print(request.data['resId'])
            if OTP.verify(request.data["otp"]):
                user.is_verified = True
                user.resId = request.data['resId']
                user.save()
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "data" : "You are authorised"
                    }
                )

            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "data" : "OTP is Wrong/Expired"
                }
            )
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "data" : "Something went wrong, try again later..."
                }
            )


class userVerify(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        id = request.data["id"]

        try:
            phoneModel.objects.get(id=id)
            return Response(
                data={True},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                data={ },
                status=status.HTTP_401_UNAUTHORIZED
            )


class Logout(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        q = f"UPDATE userlogin_phonemodel SET is_verified='0' WHERE id = '{res['userId']}'"

        with transaction.atomic():
            phoneModel.objects.raw(q)
            updated_user = phoneModel.objects.select_for_update().get(id=res['userId'])
            updated_user.is_verified = 0
            updated_user.save()
        print(updated_user)
        return Response(
            status=status.HTTP_200_OK,
            data={"message": "Successfully Updated!"}
        )
