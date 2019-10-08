# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import StandardResponse
from models.users import UsersModel, UsersSchema
from models.dataset_rg_area import DatasetAreaModel, DatasetAreaSchema
from models.projects import ProjectsModel, ProjectsSchema

class UserManager(Resource):
    @jwt_required()
    def get(self):
        # search interface
        try:
            user_instance = UsersModel.find_by_id(current_identity.id)
            user_dump, errors = UsersSchema().dump(user_instance)
            if errors:
                return StandardResponse(404, 1, u'Resource Not Found')
        except Exception, e:
            return StandardResponse(50001, 1, u'SQLAlchemy Error')
        return StandardResponse(200, 0, data=user_dump)

    @jwt_required()
    def put(self, uuid):
        # update interface
        return StandardResponse(405, 1, u'Method Not Allowed')

    @jwt_required()
    def user_delete(self, uuid):
        # delete interface
        return StandardResponse(405, 1, u'Method Not Allowed')

class UserRegister(Resource):
    def post(self):
        # register interface
        req_data = request.get_json()
        user_name = req_data.get('username', None)
        user_pass = req_data.get('password', None)
        if not user_name or not user_pass:
            return StandardResponse(403, 1, 'Forbidden')
        user = UsersModel(user_name, user_pass)
        try:
            user.add(user)
        except Exception, e:
            return StandardResponse(50001, 1, e.message)
        return StandardResponse(20001, 0, u'Create Success')

def authen_callback(username, password):
    user = UsersModel.find_by_username(username)
    return user if user and user.confirm_password(password) else None

def identity_callback(payload):
    user_identity = payload['identity']
    id = user_identity.get('useruuid', "")
    return UsersModel.find_by_id(id)

def response_callback(access_token, identity):
    data = {'Authorization': access_token.decode('utf-8'), 'user_uuid': identity.id}
    result = {'errcode': 0, 'errmsg': '', 'data': data}
    return json.dumps(result)

def payload_callback(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    user_uuid = getattr(identity, 'id') or identity['id']
    user_role = getattr(identity, 'roles') or identity['roles']
    identity = {'useruuid': user_uuid, 'userrole': user_role}
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}