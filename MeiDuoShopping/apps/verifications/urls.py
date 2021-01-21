from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    # (?P<mobile>1[3-9]\d{9})
    url(r'smscode/(?P<mobile>1[3-9]\d{9})/$', SmsCodeAPIView.as_view(), name='sms_code_view'),
]
