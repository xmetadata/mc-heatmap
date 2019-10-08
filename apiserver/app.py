# -*- coding: UTF-8 -*-
import os
import logging
from datetime import timedelta

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from common.utils import db
from resources.users import authen_callback, identity_callback, response_callback, payload_callback
from resources.users import UserManager, UserRegister
from resources.project_info import Project
from resources.project_mgr import ProjectMgr, ProjectCtl
from resources.options import Options

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
db.init_app(app)
app.config['SECRET_KEY'] = 'mch_heat_map'
app.config['JWT_AUTH_URL_RULE'] = '/apiserver/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=36000)

jwt = JWT(app, authen_callback, identity_callback)
#jwt.auth_response_handler(response_callback)
jwt.jwt_payload_handler(payload_callback)

api = Api(app)
api.add_resource(UserManager, '/apiserver/userinfo')
api.add_resource(UserRegister, '/apiserver/userigister')
api.add_resource(Project, '/apiserver/dataset')
api.add_resource(Options, '/apiserver/options')
api.add_resource(ProjectMgr, '/apiserver/project')
api.add_resource(ProjectCtl, '/apiserver/project/<string:uuid>')

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