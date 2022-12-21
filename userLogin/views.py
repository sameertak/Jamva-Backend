import base64

from django.shortcuts import render
from _datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import phoneModel
import os
from twilio.rest import Client

EXPIRY_TIME = 150


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now()))


class otpLogin(APIView):
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

        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=f"Your OTP is {OTP.now()}",
            from_="+14454557380",
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
            if OTP.verify(request.data["otp"]):
                user.is_verified = True
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