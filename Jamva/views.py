from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from Jamva import settings
from restaurant.models import restaurantModel
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.response import Response



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['role'] = self.user.groups.values_list('name', flat=True)
        print(data['role'])
        try:
            data['resId'] = (restaurantModel.objects.filter(email=self.user.username).values())[0]['resId']
            if(restaurantModel.objects.filter(email=self.user.username).values()[0]['status'] == True):
                return data
            else:
                data = {}
                return data
        except:
            return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterHere(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # try:
            username = request.data['email']
            password = request.data['password']
            resId = request.data['resId']

            try:
                restaurant = restaurantModel.objects.get(resId=resId)

            except:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={
                            'message': 'Restaurant does not exists.'
                    }
                )

            restaurant.email = username
            restaurant.save()

            try:
                users = User.objects.create_user(username=username, password=password)
                if users:
                    users.groups.add(1)
                    print(users.groups)
                    users.save()
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                                'message': 'Data is stored'
                        }
                    )
                else:
                    return Response(
                        status=status.HTTP_502_BAD_GATEWAY,
                        data={
                                'message':'Data cannot be stored, try again later'
                        }
                    )

            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'message' : 'User Already Exists'
                    }
                )
        # except:
        #     return Response(
        #         status=status.HTTP_502_BAD_GATEWAY,
        #         data={
        #             'message' : 'Provide Required Details'
        #         }
        #     )
