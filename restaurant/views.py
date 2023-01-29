import time

from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import menuModel, restaurantModel, categoryModel, orderModel
from .serializers import MenuSerializers, RestaurantSerializers, CategorySerializers, CategoryMenuSerializers, \
    OrderSerializers, FinalOrderSerializers


class RestMenu(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        q = "SELECT m.* FROM restaurant_menumodel m INNER JOIN restaurant_restaurantmodel r ON m.resId=r.id WHERE r.id=" + "'"+ str(res['resId']) + "'"
        queryset = menuModel.objects.raw(q)
        serializer = MenuSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer.data
            }

        )


class RestDetail(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        q = "SELECT * FROM restaurant_restaurantmodel WHERE id='"+str(res['resId'])+"'"
        queryset = restaurantModel.objects.raw(q)
        serializer = RestaurantSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer.data
            }
        )


class AvailabeCategory(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        q = "SELECT * FROM restaurant_categorymodel WHERE resId='" + str(res['resId']) + "'"
        queryset = categoryModel.objects.raw(q)
        serializer = CategorySerializers(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data = {
                "data" : serializer.data
            }
        )


class AddMenu(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        if list(menuModel.objects.filter(resId=res['resId'])):
            if (list(menuModel.objects.filter(foodName=res['foodName']))) == []:
                if 'image' in res.keys():
                    menuModel.objects.create(
                        resId = res['resId'],
                        category=res['category'],
                        foodName=res['foodName'],
                        description=res['description'],
                        price=res['price'],
                        image=res['image']
                    )
                else:
                    menuModel.objects.create(
                        resId=res['resId'],
                        category=res['category'],
                        description=res['description'],
                        foodName=res['foodName'],
                        price=res['price'],
                    )
            else:
                return Response(
                    data={"data": "Food Name Already Exits"}
                )

            try:

                if list(categoryModel.objects.filter(category=res['category'])) == []:

                    if 'catImage' in res.keys():
                        categoryModel.objects.create(
                            resId=res['resId'],
                            category=res['category'],
                            catImage=res['catImage']
                        )
                    else:
                        categoryModel.objects.create(
                            resId=res['resId'],
                            category=res['category'],
                        )
            except:
                return Response(
                    data={
                        "data" : "Category Already Exists"
                    }
                )

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "msg" : "Menu Successfully Updated!!"
                }
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data ={
                    "msg" : "Restaurant Not Found!!"
                }
            )


class CategoryMenu(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        try:
            q = "SELECT * FROM restaurant_menumodel WHERE resId='"+res['resId']+"' AND category='"+res['category']+"'"
            queryset = menuModel.objects.raw(q)
            serializer = CategoryMenuSerializers(queryset, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "data" : serializer.data
                }
            )

        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class UserOrder(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        global totalQuantity, totalPrice, userId, resId

        res = request.data
        userId, resId = res['userId'], res['resId']
        orderModel(
            userId=res['userId'],
            resId=res['resId'],
            foodId=res['foodId'],
            quantity=res['quantity'],
            price=res['price']
        ).save()

        q = f"SELECT * FROM restaurant_ordermodel WHERE status=False AND userId='{userId}' AND resId='{resId}'"
        queryset = orderModel.objects.raw(q)
        serializer = OrderSerializers(queryset, many=True)
        totalQuantity, totalPrice= 0, 0

        for i in serializer.data:
            totalQuantity+=i['quantity']
            totalPrice += i['price']

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : {
                    "totalQuantity" : totalQuantity,
                    "totalPrice" : totalPrice
                }
            }
        )

    @staticmethod
    def get(request):
        try:
            q = f"SELECT * FROM restaurant_ordermodel WHERE status=False AND userId='{userId}' AND resId='{resId}'"
            queryset = orderModel.objects.raw(q)
            serializer = OrderSerializers(queryset, many=True)
            totalQuantity, totalPrice = 0, 0

            for i in serializer.data:
                totalQuantity += i['quantity']
                totalPrice += i['price']
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "data": {
                        "totalQuantity": totalQuantity,
                        "totalPrice": totalPrice
                    }
                }
            )
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "data": {
                        "Error"
                    }
                }
            )


class FinalOrder(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        # q = f"SELECT o.* FROM restaurant_ordermodel o INNER JOIN restaurant_menumodel m ON o.foodId=m.id WHERE " \
        #     f"o.status='{res['status']}' AND o.userId='{res['userId']}' AND o.resId='{res['resId']}' "

        q = f"SELECT o.* FROM restaurant_ordermodel o INNER JOIN restaurant_menumodel m ON o.foodId=m.id WHERE o.status='{res['status']}' AND o.userId='{res['userId']}' AND o.resId='{res['resId']}'"
        queryset = orderModel.objects.raw(q)
        serializer1 = FinalOrderSerializers(queryset, many=True)
        print(serializer1.data)

        q = f"SELECT m.* FROM restaurant_menumodel m INNER JOIN restaurant_ordermodel o ON m.id=o.foodId WHERE o.status='{res['status']}' AND o.userId='{res['userId']}' AND o.resId='{res['resId']}'"
        queryset = menuModel.objects.raw(q)
        serializer2 = MenuSerializers(queryset)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer.data
            }
        )
    # @staticmethod
    # def post(request):
    #     res = request.data
    #     print(res)
    #     temp = ""
    #     for id_ in res['oderedItems']:
    #         id_.value()
    #         temp+=f"{id},"
    #         print(temp)
    #     return Response(
    #         data={
    #             "data" : res
    #         }
    #     )