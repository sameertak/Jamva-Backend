import time
import os 
import uuid

from django.db import transaction
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import menuModel, restaurantModel, categoryModel, orderModel, employeeModel
from userLogin.models import phoneModel, userModel, CardDetail
from .serializers import MenuSerializers, RestaurantSerializers, CategorySerializers, CategoryMenuSerializers, \
    OrderSerializers, OrderSerializer, FinalOrderSerializers, CustomerSerializers, OrderCustomerSerializer, \
    MenuManageSerializers, RestaurantDetailSerializer, TotalPriceSerializers, EmployeeSerializers
from collections import defaultdict

class RestMenu(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        q = "SELECT m.* FROM restaurant_menumodel m INNER JOIN restaurant_restaurantmodel r ON m.resId=r.resId WHERE r.resId=" + "'"+ str(res['resId']) + "'"
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

        q = "SELECT * FROM restaurant_restaurantmodel WHERE resId='"+str(res['resId'])+"'"
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
        image_file = request.FILES.get('image', None)

        def generate_filename(filename):
            base_filename, file_extension = os.path.splitext(filename)
            return base_filename + '_' + str(uuid.uuid4()) + file_extension

        print(list(restaurantModel.objects.filter(resId=res['resId'])))
        if list(restaurantModel.objects.filter(resId=res['resId'])):
            if (list(menuModel.objects.filter(foodName=res['foodName'], resId=res['resId']))) == []:
                if image_file:
                    filename = generate_filename(image_file.name)
                    with open(os.path.join('media', filename), 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                # if 'image' in res.keys():
                    print('1')
                    menuModel.objects.create(
                        cat_id = res['catId'],
                        resId = res['resId'],
                        category=res['category'],
                        foodName=res['foodName'],
                        description=res['description'],
                        price=res['price'],
                        image=filename
                        # image=img
                    )
                else:
                    print('2')

                    menuModel.objects.create(
                        cat_id=res['catId'],
                        resId=res['resId'],
                        category=res['category'],
                        description=res['description'],
                        foodName=res['foodName'],
                        price=res['price'],
                    )
            else:
                return Response(
                    data={"message": "Food Name Already Exits"}
                )

            try:

                if list(categoryModel.objects.filter(cat_id=res['catId'])) == []:
                    print('3')

                    if 'catImage' in res.keys():
                        categoryModel.objects.create(
                        cat_id = res['catId'],
                            resId=res['resId'],
                            category=res['category'],
                            catImage=res['catImage']
                        )
                    else:
                        categoryModel.objects.create(
                        cat_id = res['catId'],
                            resId=res['resId'],
                            category=res['category'],
                        )
            except:
                return Response(
                    data={
                        "message" : "Category Already Exists"
                    }
                )

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message" : "Menu Successfully Updated!!"
                }
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data ={
                    "message" : "Restaurant Not Found!!"
                }
            )


class CategoryMenu(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        # try:
        q = "SELECT m.*,c.* FROM restaurant_menumodel m INNER JOIN restaurant_categorymodel c ON m.cat_id=c.id WHERE m.resId='"+res['resId']+"' AND c.category='"+res['category']+"'"
        queryset = menuModel.objects.raw(q)
        serializer = CategoryMenuSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer.data
            }
        )
        #
        # except:
        #     return Response(
        #         status=status.HTTP_404_NOT_FOUND
        #     )


class UserOrder(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        global totalQuantity, totalPrice, userId, resId

        res = request.data
        userId, resId, foodId = res['userId'], res['resId'], res['foodId']
        orderModel(
            customer = phoneModel.objects.get(id=userId),
            userId=res['userId'],
            resId=res['resId'],
            foodId= menuModel.objects.get(id=foodId),
            quantity=res['quantity'],
            price=res['price'],
            info=res['info']
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

        q = f"SELECT o.* FROM restaurant_ordermodel o INNER JOIN restaurant_menumodel m ON o.foodId_id=m.id WHERE o.status='{res['status']}' AND o.userId='{res['userId']}' AND o.resId='{res['resId']}'"
        queryset = orderModel.objects.raw(q)
        serializer1 = FinalOrderSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer1.data
            }
        )


class AllRestaurants(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        q="SELECT * FROM restaurant_restaurantmodel"

        queryset = restaurantModel.objects.raw(q)
        serializer = RestaurantSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data = {
                "data" : serializer.data
            }
        )


class GetRestaurantNameById(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        response = request.data
        restaurant = response['resId']

        try:
            restaurantName = restaurantModel.objects.get(resId=restaurant)

            return Response(
                status = status.HTTP_200_OK,
                data = {
                    "message": restaurantName.name
                }
            )

        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message" : "Restaurant doesn't exists"
                }
            )

class RegisterRestaurant(APIView):
    permission_classes = [AllowAny]


    @staticmethod
    def post(request):
        response = request.data

        resId = response['resId']
        try:
            try:
                restaurantModel.objects.get(resId=resId)
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={
                        "success" : "false",
                        "message" : "Restaurant already exists"
                    }
                )
            except:
                x = restaurantModel.objects.create(
                    resId = resId,
                    name = response['name'],
                    manager = response['manager'],
                    contact = response['contact'],
                    email = response['email'],
                    social = response['social']
                )

                if (x==None):
                    return Response(
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={
                            "success" : "false",
                            "message" : "Oops! The Restaurant could not be added!"
                        }
                    )
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "success" : "true",
                        "message" : "Restaurant added successfully!"
                    }
                )
        except:
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                data={
                    "success" : "false",
                    "message" : "Please provide correct details!"
                }
            )
# class FinalOrder(APIView):
#     @staticmethod
#     def post(request):
#         res = request.data
#
#         list_of_items = res['foodItemIds']
#
#         q = f"SELECT * FROM restaurant_menumodels WHERE id in {tuple(list_of_items)}"
#         queryset = menuModel.objects.raw(q)
#         serializer = MenuSerializers(queryset, many=True)
#
#
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

class NameToIdCat(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        category = request.data['category']
        resId = request.data['resId']


        value = categoryModel.objects.filter(category=category, resId=resId).values()
        if (str(value) == '<QuerySet []>'):
            categoryModel.objects.create(
                category=category,
                resId=resId
            )


        return Response(
            status=status.HTTP_200_OK,
            data={'category': value[0]['id']}
        )


class CustomerList(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        resId = request.data['resId']
        q=f"SELECT SUM(quantity) as total_quantity, o.*, p.* FROM restaurant_ordermodel o INNER JOIN userlogin_phoneModel p ON o.customer_id = p.id WHERE o.resId = '{resId}' GROUP BY userId ORDER BY created_at DESC"
        queryset = orderModel.objects.raw(q)
        # print(queryset)
        serializer1 = OrderCustomerSerializer(queryset, many=True)
        # serializer2 = CustomerSerializers(queryset, many=True)
        # data = {
        #     'orders': serializer1.data,
        #     'customers': serializer2.data
        # }
        # for key in serializer1.data:
        # for i in range(len(serializer1.data)):
        #     serializer1.data[i].update(serializer2.data[i])


        return Response(
            status=status.HTTP_200_OK,
            data=serializer1.data
        )


class UpdateItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data
        # Update the order
        q = f"UPDATE restaurant_ordermodel SET quantity = '{res['quantity']}', info = '{res['info']}' WHERE id = '{res['id']}'"
        queryset = orderModel.objects.raw(q)
        print(queryset)
        with transaction.atomic():
            orderModel.objects.raw(q)
            updated_order = orderModel.objects.select_for_update().get(id=res['id'])
            updated_order.quantity = res['quantity']
            updated_order.info = res['info']
            updated_order.save()
        # Serialize the updated object
        serializer = FinalOrderSerializers(updated_order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data

        q = f"DELETE FROM restaurant_ordermodel WHERE id = {res['id']}"
        queryset = orderModel.objects.raw(q)
        with transaction.atomic():
            orderModel.objects.raw(q)
            updated_order = orderModel.objects.select_for_update().get(id=res['id'])
            # updated_order.quantity = res['quantity']
            # updated_order.info = res['info']
            updated_order.delete()
        # Serialize the updated object
        serializer = FinalOrderSerializers(updated_order)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserDetail(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        q = f"SELECT o.*, p.*, m.foodName FROM restaurant_ordermodel o INNER JOIN userlogin_phoneModel p ON o.customer_id = p.id INNER JOIN restaurant_menuModel m ON o.foodId_id = m.id WHERE o.resId = '{res['resId']}' AND o.customer_id='{res['userId']}' ORDER BY created_at DESC"
        # print(q)
        # queryset = orderModel.objects.raw(q)
        #

        # q = f"SELECT o.*, p.* FROM restaurant_ordermodel o INNER JOIN userlogin_phoneModel p ON o.resId = p.resId WHERE o.resId = '{res['resId']}' AND o.userId='{res['userId']}'"

        # print(orderModel.objects.get(foodId=1))
        queryset = orderModel.objects.raw(q)

        # serializer1 = MenuSerializers(queryset, many=True)
        # serializer2 = CustomerSerializers(queryset, many=True)
        # serializer3 = OrderSerializer(queryset, many=True)
        #
        # print(serializer1.data)
        # for i in range(len(serializer1.data)):
        #     serializer1.data[i].update(serializer2.data[i])
        #     serializer1.data[i].update(serializer3.data[i])
        #

        serializer = OrderSerializer(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

class ManageMenu(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data

        q = """SELECT m.*
                FROM restaurant_menumodel m 
                INNER JOIN restaurant_restaurantmodel r 
                ON m.resId=r.resId 
                WHERE r.resId='""" + res["resId"] + """' 
                """
        print(q)
        queryset = menuModel.objects.raw(q)
        serializer = MenuManageSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "data" : serializer.data
            }

        )

class FoodMenu(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data
        foodId = res['foodId']

        q = f'SELECT * FROM restaurant_menumodel WHERE id={foodId}'
        queryset = menuModel.objects.raw(q)

        serializer = MenuSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class UpdateMenuItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data
        # Update the order
        q = f"UPDATE restaurant_menumodel SET cat_id = '{res['catId']}', foodName = '{res['foodName']}', description = '{res['description']}, price='{res['price']}' WHERE id = '{res['foodId']}'"
        queryset = menuModel.objects.raw(q)
        print(queryset)
        with transaction.atomic():
            menuModel.objects.raw(q)
            updated_menu = menuModel.objects.select_for_update().get(id=res['foodId'])
            updated_menu.cat_id = res['catId']
            updated_menu.foodName = res['foodName']
            updated_menu.description = res['description']
            updated_menu.price = res['price']
            updated_menu.save()
        # Serialize the updated object
        serializer = MenuSerializers(updated_menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteMenuItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data

        q = f"DELETE FROM restaurant_menumodel WHERE id = {res['foodId']}"
        with transaction.atomic():
            menuModel.objects.raw(q)
            updated_order = menuModel.objects.select_for_update().get(id=res['foodId'])
            updated_order.delete()
        # Serialize the updated object
        serializer = MenuSerializers(updated_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurantDetail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data
        q = f"SELECT * from restaurant_restaurantmodel r INNER JOIN restaurant_menuModel m ON r.resId=m.resId WHERE r.id = '{res['resId']}'"
        queryset1 = restaurantModel.objects.raw(q)
        queryset2 = menuModel.objects.raw(q)

        serializer1 = RestaurantDetailSerializer(queryset1, many=True)
        serializer2 = MenuSerializers(queryset2, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data = {"restaurant":serializer1.data, "menu":serializer2.data}
        )

#
# class Totals(APIView):
#     permission_classes = [AllowAny]
#
#     @staticmethod
#     def post(request):
#         res = request.data
#
#

class SetStatus(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data['checkedItems']
        print(res)
        if res!={}:
            for i in res:
                q = f"UPDATE restaurant_restaurantmodel SET status={res[i]} WHERE resId={i}"

            with transaction.atomic():
                restaurantModel.objects.raw(q)
                updated_res = restaurantModel.objects.select_for_update().get(resId=i)
                updated_res.status = res[i]
                updated_res.save()

            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Successfully Updated!"}
            )
        if (res == {}):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Bad Request, Try Again Later"}
            )

class CheckStatus(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        
        return Response(
            status=status.HTTP_200_OK,
            data={"message": restaurantModel.objects.filter(resId=res['resId']).values()[0]['status']}
        )

class CardPayment(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        try:
            CardDetail.objects.get(name=res['name'] ,cardNo=res['card'], cvv=res['cvv'], expiry=res['expiry'])
            return Response(
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )


class GetTotalPrice(APIView):
    permission_classes=[AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        q = f"SELECT id, SUM(price) AS total_price, SUM(quantity) AS total_quantity FROM restaurant_ordermodel WHERE resId='{res['resId']}' AND userId='{res['userId']}' AND status=0"
        queryset = orderModel.objects.raw(q)
        serializer = TotalPriceSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

class UpdateItemStatus(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        res = request.data
        print(res)
        for i in range(len(res['food'])):
            counter = res['food'][i]['quantity']
            counter += res['food'][i]['foodId']['counter']
            q = f"UPDATE restaurant_menumodel SET counter='{counter}' WHERE id = '{res['food'][i]['foodId']['id']}'"
            queryset = menuModel.objects.raw(q)
            with transaction.atomic():
                menuModel.objects.raw(q)
                updated_order = menuModel.objects.select_for_update().get(id=res['food'][i]['foodId']['id'])
                updated_order.counter += res['food'][i]['quantity']
                updated_order.save()

            # Update the order
            q = f"UPDATE restaurant_ordermodel SET status = '1' WHERE id = '{res['food'][i]['id']}'"
            queryset = orderModel.objects.raw(q)
            with transaction.atomic():
                orderModel.objects.raw(q)
                updated_order = orderModel.objects.select_for_update().get(id=res['food'][i]['id'])
                updated_order.status = 1
                updated_order.save()
            # Serialize the updated object
        return Response(status=status.HTTP_200_OK)

class TrendingItem(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data
        q = f"SELECT * FROM restaurant_menumodel WHERE resId='{res['resId']}' ORDER BY counter DESC LIMIT 5"
        queryset = menuModel.objects.raw(q)
        serializer1 = MenuSerializers(queryset, many=True)

        q = f"SELECT * FROM (SELECT DISTINCT foodId_id, * FROM restaurant_ordermodel WHERE resId='{res['resId']}' AND userId='{res['userId']}') AS temp WHERE (foodId_id, updated_at) IN (SELECT foodId_id, MAX(updated_at) FROM restaurant_ordermodel WHERE resId='{res['resId']}' AND userId='{res['userId']}' GROUP BY foodId_id) ORDER BY updated_at DESC LIMIT 5;"
        queryset = orderModel.objects.raw(q)
        serializer2 = FinalOrderSerializers(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=[serializer1.data, serializer2.data]
        )

class ConfmOrder(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data

        q=f"SELECT * FROM restaurant_ordermodel WHERE userId='{res['userId']}' AND resId='{res['resId']}' AND status='1' ORDER BY updated_at DESC"
        queryset = orderModel.objects.raw(q)
        serializer = FinalOrderSerializers(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data = serializer.data
        )


class RestaurantDetailsAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        q = f"SELECT * FROM restaurant_restaurantmodel WHERE resId='{res['resId']}'"
        queryset = restaurantModel.objects.raw(q)
        serializer = RestaurantSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class EmployeeDetail(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data
        resId=res['resId']


        q = f"SELECT * FROM restaurant_employeemodel WHERE resId='{resId}'"
        queryset = employeeModel.objects.raw(q)

        serializer = EmployeeSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class EmployeeAdd(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data

        employeeModel(
            resId=res['resId'],
            designation=res['designation'],
            name=res['name'],
            salary=res['salary'],
        ).save()

        return Response(
            status=status.HTTP_200_OK
        )

class EmployeeGet(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        res = request.data

        q = f"SELECT * FROM restaurant_employeemodel WHERE id='{res['id']}'"
        queryset = employeeModel.objects.raw(q)
        serializer = EmployeeSerializers(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class EmployeeEdit(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        with transaction.atomic():
            updated_emp = employeeModel.objects.select_for_update().get(id=res['id'])
            updated_emp.name = res['name']
            updated_emp.salary = res['salary']
            updated_emp.designation = res['designation']
            updated_emp.save()

        return Response(
            status=status.HTTP_200_OK
        )

class EmployeeDelete(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        with transaction.atomic():
            delete_emp = employeeModel.objects.select_for_update().get(id=res['id'])
            delete_emp.delete()

        return Response(
            status=status.HTTP_200_OK
        )


class SetTableNo(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        res = request.data
        with transaction.atomic():
            set_table = orderModel.objects.select_for_update().get(id=res['id'])
            set_table.table = res['tableNo']

        return Response(
            status=status.HTTP_200_OK
        )