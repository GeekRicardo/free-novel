#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  config.py
@Time     :  2020/10/23 16:36:59
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  配置项
'''

# import lib here
import os
import datetime

# from loguru import logger

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JSON_AS_ASCII = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[QingLingXiaoShuo]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    CACHE_TYPE = "simple"


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    "mysql://root:ricardo@localhost:3306/Ricardo?charset=utf8"
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(seconds=5)

config ={
    'development': DevelopmentConfig
}
