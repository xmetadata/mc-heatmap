# -*- coding: UTF-8 -*-
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


class Users(Resource):
    @jwt_required()
    def get(self, uuid):
        #search interface
        if current_identity.roless not in ['super'] and \
            uuid != current_identity.id:
            return StandardResponse(403, 1, '非管理员, 无权限')
        user_instance = UsersModel.query.get_or_404(uuid)
        user_dump, errors = UsersSchema().dump(user_instance)
        if errors:
            return StandardResponse(404, 1, '不能找到指定用户')
        return StandardResponse(200, 0, data = user_dump)

    def post(self):
        #register interface
        user_name = request.form['username']
        user_pass = request.form['password']
        if not user_name or not user_pass:
            return StandardResponse(406, 1, '无效的用户名或密码')
        user = UsersModel(user_name, user_pass)
        try:
            user.add(user)
        except Exception, e:
            return StandardResponse(412, 1, e.message)
        return StandardResponse(200)

    @jwt_required()
    def put(self, uuid):
        #update interface
        if current_identity.roless not in ['super'] and \
            uuid != current_identity.id:
            return StandardResponse(403, 1, '非管理员, 无权限')
        users_instance = UsersModel.query.get_or_404(uuid)
        try:
            jsondata = request.get_json()
            data, errors = UsersSchema().load(jsondata)
            if errors:
                current_app.logger.error(errors)
                return pretty_response(40003)
            for key, value in jsondata.items():
                setattr(users_instance, key, value)
            users_instance.updatetime = datetime.now()
            users_instance.update()
            users_dump, errors = UsersSchema().dump(users_instance)
            return pretty_response(200, users_dump)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)

    @jwt_required()
    def delete(self, uuid):
        #delete interface
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        users_instance = UsersModel.query.get_or_404(uuid)
        try:
            users_instance.delete(users_instance)
            return pretty_response(20003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)
