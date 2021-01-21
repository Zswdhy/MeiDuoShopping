from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

from rest_framework import generics


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer


# 失去焦点的时候，前端立马作出相应
# 此接口，仅返回 user 的数量，数量交付给前端，前端做处理，数量为1，已经存在，数量为0，不存在，可以注册
class UsernameValidatePIView(APIView):
    def get(self, request, username):
        print('query_params', request.query_params)
        print('data', request.data)
        print('parsers', request.parsers)
        user = Users.objects.filter(username=username).count()
        res = {
            'username': username,
            'count': user
        }
        return Response(res)


# 失去焦点的时候，前端立马作出相应
# 此接口，仅返回 mobile 的数量，数量交付给前端，前端做处理
class MobileValidatePIView(APIView):
    def get(self, request, mobile):
        user = Users.objects.filter(mobile=mobile).count()
        res = {
            'username': mobile,
            'count': user
        }
        return Response(res)
