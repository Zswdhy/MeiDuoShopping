from django.contrib.auth.backends import ModelBackend
import re
from .models import Users


def jwt_response_payload_handler(token, user=None, request=None):
    # 在 settings 内修改 JWT_AUTH JWT_RESPONSE_PAYLOAD_HANDLER 的路由地址，即可以使用本地重写的方法
    """重写JWT登录视图的构造响应数据函数,多追加 user_id和 username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    通过传入的账号动态获取user 模型对象
    :param account:  有可以是手机号,有可能是用户名
    :return:  user或None
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            user = Users.objects.get(mobile=account)
        else:
            user = Users.objects.get(username=account)
    except Users.DoesNotExist:
        return None  # 如果没有查到返回None
    else:
        return user  # 注意不要写在模型类


# 需要在 settings.py文件中重新配置 django后端认证的类 AUTHENTICATION_BACKENDS
class UsernameMobileAuthBackend(ModelBackend):
    """修改Django的认证类,为了实现多账号登录，重写认证方法"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取到user
        user = get_user_by_account(username)
        # 判断当前前端传入的密码是否正确
        if user and user.check_password(password):
            # 返回user
            return user
