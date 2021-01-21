from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer


# 失去焦点的时候，前端立马作出相应
# 此接口，仅返回 user 的数量，数量交付给前端，前端做处理，数量为1，已经存在，数量为0，不存在，可以注册
class UsernameValidatePIView(APIView):
    def get(self, request, username):
        # print('query_params', request.query_params)
        # print('data', request.data)
        # print('parsers', request.parsers)
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


class UserDetailView(RetrieveAPIView):
    # RetrieveAPIView 只返回一条数据，不需要重写get方法
    """用户详情信息展示"""
    serializer_class = UserDetailSerializer
    # queryset = Users.objects.all() # url  后面需要拼接pk进行查询，这样沪造成服务器压力过大
    permission_classes = [IsAuthenticated, ]  # 指定权限

    # 重写父类方式
    def get_object(self):
        """重写方式，返回展示的用户实例"""
        return self.request.user


# put  请求
class EmailView(UpdateAPIView):
    """更新用户邮箱"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = EmailSerializer

    #  直接返回用户模型实例，无须定义查询集，减少数据库查询
    def get_object(self):
        return self.request.user
