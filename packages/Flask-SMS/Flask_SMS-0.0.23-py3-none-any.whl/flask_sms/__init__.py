"""
 Flask-SMS
 # ~~~~~~~~~~~~~~ 
 flask 短信 扩展
 Flask SMS extension
 :copyright: (c) 2023.11 by 浩. 
 :license: GPL, see LICENSE for more details.
"""

import os
import random
import string
from datetime import datetime

import redis

from .aliyun_send import Sample


# 限制短信频率


class SMS(object):
    def __init__(self, app=None, **kwargs):
        self.app = app

        if app is not None:
            print("init_app")
            self.init_app(app, **kwargs)
            self.app = app



    def init_app(self, app):
        # 兼容 0.7 以前版本
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        # 在 app 应用中存储所有扩展实例, 可验证扩展是否完成实例化
        app.extensions['sms'] = self

        # 扩展配置， 初始化后添加到 app.config 中, 以 SHARE_ 开头避免冲突
        app.config.setdefault('SMS_REDIS_HOST', '127.0.0.1')
        app.config.setdefault('SMS_REDIS_PORT', 6379)
        app.config.setdefault('SMS_REDIS_DB', 0)
        app.config.setdefault('SMS_REDIS_PASSWORD', None)
        app.config.setdefault('SMS_REDIS_INSTANCE', None)

        # 设置 Redis 键的过期时间来限制发送频率
        app.config.setdefault('SMS_RATE_LIMIT', 60)
        # 设置每天最大发送次数
        app.config.setdefault('SMS_DAILY_LIMIT', 5)

        # 设置阿里云短信参数
        # 短信签名名称
        app.config.setdefault('SMS_ALIYUN_SMS_SIGN_NAME', None)
        # 短信模板Code
        app.config.setdefault('SMS_ALIYUN_SMS_TEMPLATE_CODE', 1)

        # 设置阿里云短信 AccessKey
        app.config.setdefault('SMS_ALIYUN_ACCESS_KEY_ID', '')
        app.config.setdefault('SMS_ALIYUN_ACCESS_KEY_SECRET', '')

    def send_aliyun_sms(self, phone, template_param):
        """
        发送阿里云短信

        """
        d = {

            "phone": phone,
            # TemplateParam 短信模板变量对应的实际值
            "template_param": template_param
        }
        # if not self.limit_sms_frequency(phone):
        #     return False

        return Sample.main(self.app, d)

    @staticmethod
    def code():
        characters = string.digits  # 使用数字作为验证码的字符集合
        code = ''.join(random.choice(characters) for _ in range(4))  # 从字符集合中随机选择4个字符

        return code

    # def create_redis_instance(self,app):
    #     redis_instance = redis.Redis(
    #         host=app.config.get("SMS_REDIS_HOST"),
    #         port=app.config.get("SMS_REDIS_PORT"),
    #         db=self.app.config.get("SMS_REDIS_DB"),
    #         password=self.app.config.get("SMS_REDIS_PASSWORD"),
    #     )

    # self.app.sms_redis_instance = redis_instance

    # def limit_sms_frequency(self, phone,app=None):
    #     redis_instance = app.sms_redis_instance
    #
    #     # 设置限制，例如每分钟只能发送一次  秒
    #     limit = app.config.get("SMS_RATE_LIMIT")
    #     # 设置每天最大发送次数
    #     max_daily_limit = app.config.get("SMS_DAILY_LIMIT")
    #
    #     key = "sms_rate_limit:{phone}".format(phone=phone)
    #
    #     if redis_instance.exists(key):
    #         print("sms_rate_limit:{phone}".format(phone=phone))
    #         return False
    #
    #     # 设置 Redis 键的过期时间来限制发送频率
    #     redis_instance.setex(key, limit, 1)
    #
    #     current_date = datetime.now().strftime("%Y-%m-%d")
    #
    #     key = "sms_daily_limit:{phone_number}:{current_date}".format(phone_number=phone, current_date=current_date)
    #
    #     # 获取当前手机号今天已发送的次数
    #     current_count = redis_instance.get(key)
    #     if current_count is None:
    #         # 如果还没有发送记录，设置计数为1，并设置过期时间为到今天结束
    #         ttl = 86400 - datetime.now().second - datetime.now().minute * 60 - datetime.now().hour * 3600
    #         redis_instance.setex(key, ttl, 1)
    #
    #         return True
    #     else:
    #         current_count = int(current_count)
    #         if current_count >= max_daily_limit:
    #             # 如果已达到或超过每天的限制，则不能发送
    #             print("手机号{phone}今天发送次数已达到{count}次，请明天再试")
    #             return False
    #         else:
    #             # 如果没有达到每天的限制，增加发送次数
    #             redis_instance.incr(key)
    #             return True
