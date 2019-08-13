# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import pretty_response
from models.users import UsersModel, UsersSchema


class UsersList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
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
        """ Query specific instance """
        if current_identity.roless not in ['super'] and \
            uuid != current_identity.id:
            return pretty_response(403)
        users_instance = UsersModel.query.get_or_404(uuid)
        users_dump, errors = UsersSchema().dump(users_instance)
        return pretty_response(200, users_dump)

    def post(self, uuid):
        """ Update specific instance """
        return pretty_response(405)

    @jwt_required()
    def put(self, uuid):
        """ Update specific instance """
        if current_identity.roless not in ['super'] and \
            uuid != current_identity.id:
            return pretty_response(403)
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
        """ Delete specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        users_instance = UsersModel.query.get_or_404(uuid)
        try:
            users_instance.delete(users_instance)
            return pretty_response(20003)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(50001)
