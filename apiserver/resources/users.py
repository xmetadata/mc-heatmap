# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import pretty_response
from common.utils import StandardResponse
from models.users import UsersModel, UsersSchema

class UsersList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return StandardResponse(404, 1, '非超级用户, 无权限')
        users_list = UsersModel.query.all()
        users_dump, errors = UsersSchema(many=True).dump(users_list)
        return pretty_response(200, users_dump)

    def post(self):
        """ Insert multi-instances """
        jsondata = request.get_json()
        if not jsondata or jsondata['username'] is None:
            return pretty_response(40001)
        if UsersModel.query.filter_by(username=jsondata['username']).first():
            return pretty_response(40002)
        try:
            users_instance, errors = UsersSchema().load(jsondata)
            if errors:
                current_app.logger.error(errors)
                return pretty_response(40003)
            password = jsondata['password']
            users_instance = UsersModel(jsondata['username'], password)
            users_instance.add(users_instance)
            users_dump, errors = UsersSchema().dump(users_instance)
            return pretty_response(200, users_dump)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)

    def put(self):
        """ Update multi-instances """
        return pretty_response(405)

    def delete(self):
        """ Batch-delete instances """
        return pretty_response(405)

class UserManager(Resource):
    @jwt_required()
    def get(self, uuid):
        # search interface
        if current_identity.roless not in ['super'] and \
                uuid != current_identity.id:
            return StandardResponse(403, 1, '非管理员, 无权限')
        user_instance = UsersModel.query.get_or_404(uuid)
        user_dump, errors = UsersSchema().dump(user_instance)
        if errors:
            return StandardResponse(404, 1, '不能找到指定用户')
        return StandardResponse(200, 0, data=user_dump)

    @jwt_required()
    def put(self, uuid):
        # update interface
        try:
            users_instance = UsersModel.query.get_or_404(uuid)
            if not users_instance:
                return StandardResponse(404, 1, '无效的用户ID')
            json_data = request.get_json()
            data, errors = UsersSchema().load(json_data)
            if errors:
                current_app.logger.error(errors)
                return StandardResponse(500, 1, '用户序列化失败')
            for key, value in json_data.items():
                setattr(users_instance, key, value)
            users_instance.updatetime = datetime.now()
            users_instance.update()
            users_dump, errors = UsersSchema().dump(users_instance)
            if errors:
                users_instance.roolback()
                return StandardResponse(500, 1, '更新用户序列化失败')
            return StandardResponse(200, 0, data=users_dump)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return StandardResponse(500, 1, e.message)

    @jwt_required()
    def user_delete(self, uuid):
        # delete interface
        if current_identity.roles not in ['super']:
            return StandardResponse(403, 1, '非管理员，无权限')
        try:
            users_instance = UsersModel.query.get_or_404(uuid)
            if not users_instance:
                return StandardResponse(404, 1, '无效的用户ID')
            users_instance.delete(users_instance)
            return StandardResponse(200, 0)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return StandardResponse(500, 1, e.message)

class UserRegister(Resource):
    def post(self):
        # register interface
        req_data = request.get_json()
        user_name = req_data.get('username', None)
        user_pass = req_data.get('password', None)
        if not user_name or not user_pass:
            return StandardResponse(406, 1, '无效的用户名或密码')
        user = UsersModel(user_name, user_pass)
        try:
            user.add(user)
        except Exception, e:
            return StandardResponse(412, 1, e.message)
        return StandardResponse(200)

def authen_callback(username, password):
    user = UsersModel.find_by_username(username)
    return user if user and user.confirm_password(password) else None

def identity_callback(payload):
    id = payload['identity']
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