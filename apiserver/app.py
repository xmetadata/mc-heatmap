# -*- coding: UTF-8 -*-
import logging
import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from common.utils import db
from resources.options import Options, OptionsList
from resources.users import Users, UsersList
from models.users import UsersModel

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
app.config['SECRET_KEY'] = 'mch_heat_map'

def authenticate(cls, username, password):
    user = UsersModel.find_by_username(username)
    return user if user and user.confirm_password(password) else None

def identity(cls, payload):
    id = payload['identity']
    return UsersModel.find_by_id(id)

jwt = JWT(app, authenticate, identity)

api = Api(app)
#api.add_resource(Options, '/apiserver/v1.0/options/<string:uuid>')
#api.add_resource(OptionsList, '/apiserver/v1.0/options')
#api.add_resource(UsersList, '/apiserver/v1.0/users')
api.add_resource(Users, '/apiserver/v1.0/register')

if __name__ == '__main__':
    logpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    handler = logging.FileHandler(os.path.join(logpath, 'apiserver.log'),
                                  encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])