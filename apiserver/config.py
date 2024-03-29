# -*- coding: UTF-8 -*-
import os
from datetime import timedelta


class Config(object):
    # Server
    HOST = "0.0.0.0"
    PORT = 5050

    # JWT
    SECRET_KEY = "apiserver is porwered by xmetadata"
    JWT_EXPIRATION_DELTA = timedelta(seconds=36000)
    JWT_AUTH_URL_RULE = '/apiserver/v1.0/auth'


class ProductionConfig(Config):
    # Server
    DEBUG = True

    # MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aa888888@47.103.36.82:3306/heatmap?charset=utf8'
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_MAX_OVERFLOW = 10

class DevelopmentConfig(Config):
    # Server
    DEBUG = True

    # SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/data/databases.db' % os.path.dirname(
        os.path.realpath(__file__))
