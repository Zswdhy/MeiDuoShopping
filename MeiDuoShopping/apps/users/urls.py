from django.conf.urls import url
from .views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'users/$', UserView.as_view()),
    url(r'^username/(?P<username>\w+)/$', UsernameValidatePIView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/$', MobileValidatePIView.as_view()),
    # 在 utils 工具包内，
    url(r'login/', obtain_jwt_token),  # rest frame work jwt 内置登陆，自动返回 jwt token

    url(r'user/$', UserDetailView.as_view()),  # 获取用户详情，在个人中心展示
    url(r'email/$', EmailView.as_view())  # 更新邮箱
]
