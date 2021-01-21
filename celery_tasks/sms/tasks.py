# 异步任务代码
# from celery_tasks import CCP
from .constants import *
from .yuntongxun.sms import CCP
from ..main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, ):
    CCP().send_template_sms(mobile, [sms_code, SMS_CODE_REDIS_EXPIRES // 60], 1)
