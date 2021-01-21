from rest_framework import serializers
from .models import Users
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


class CreateUserSerializer(serializers.ModelSerializer):
    # abstract_user 中不存在的字段
    password2 = serializers.CharField(write_only=True)
    sms_code = serializers.CharField(write_only=True)
    allow = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 32,
                'error_messages': {
                    'min_length': '仅允许5-32个字符的用户名',
                    'max_length': '仅允许5-32个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 5,
                'max_length': 32,
                'error_messages': {
                    'min_length': '仅允许5-32个字符的密码',
                    'max_length': '仅允许5-32个字符的密码',
                }
            },
        }

    # 校验单独字段
    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('请同意协议')
        return value

    # 校验多个字段
    def validate(self, attrs):
        """
        :param attrs: 前端提交的表单数据
        :return:
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入的密码不一致')

        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get(f'sms_{mobile}')

        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证那错误')
        return attrs

    # 创建user
    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        # 明文
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()

        # 注册后直接生成 token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt
        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt
        user.token = token

        return user
