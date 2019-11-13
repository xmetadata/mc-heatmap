# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import pretty_response, StandardResponse
from models.options import OptionsModel, OptionsSchema


class OptionsList(Resource):
    @jwt_required()
    def get(self):
        """ Query all instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        try:
            if request.args.get('opt_key'):
                options_list = OptionsModel.query.filter_by(
                    opt_key=request.args.get('opt_key')).all()
            else:
                options_list = OptionsModel.query.all()
            options_dump, errors = OptionsSchema(many=True).dump(options_list)
            return pretty_response(200, options_dump)
        except Exception, e:
            return pretty_response(500, 1, e.message)

    @jwt_required()
    def post(self):
        """ Insert multi-instances """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        jsondata = request.get_json()
        if not jsondata or 'opt_key' not in jsondata:
            return pretty_response(400)
        if OptionsModel.query.filter_by(opt_key=jsondata['opt_key']).first():
            return pretty_response(400)
        try:
            options_instance, errors = OptionsSchema().load(jsondata)
            if errors:
                current_app.logger.error(errors)
                return pretty_response(400)
            options_instance.add(options_instance)
            options_dump, errors = OptionsSchema().dump(options_instance)
            return pretty_response(200, options_dump)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            return pretty_response(500)

    def put(self):
        """ Update multi-instances """
        return pretty_response(405)

    def delete(self):
        """ Batch-delete instances """
        return pretty_response(405)


class Options(Resource):
    @jwt_required()
    def get(self):
        """ Query specific instance """
        if current_identity.roles not in ['super']:
            return pretty_response(403)
        options_instance = None
        try:
            if request.args.get('opt_key'):
                options_instance = OptionsModel.query.filter(OptionsModel.opt_key == request.args.get('opt_key')).first()
            else:
                return StandardResponse(400, 1, u'Invalid Request Parameters')
        except Exception, e:
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        if not options_instance:
            return StandardResponse(500, 1, u'Invalid request Parameters')
        return StandardResponse(200, 0, data = options_instance.opt_value)

    @jwt_required()
    def post(self):
        """ Update specific instance """
        return pretty_response(405)

    # @jwt_required()
    # def put(self, uuid):
    #     """ Update specific instance """
    #     if current_identity.roles not in ['super']:
    #         return pretty_response(403)
    #     options_instance = OptionsModel.query.get_or_404(uuid)
    #     try:
    #         jsondata = request.get_json()
    #         data, errors = OptionsSchema().load(jsondata)
    #         if errors:
    #             current_app.logger.error(errors)
    #             return pretty_response(40003)
    #         for key, val in jsondata.items():
    #             setattr(options_instance, key, val)
    #         options_instance.updatetime = datetime.now()
    #         options_instance.update()
    #         options_dump, errors = OptionsSchema().dump(options_instance)
    #         return pretty_response(200, options_dump)
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(e)
    #         return pretty_response(50001)
    #
    # @jwt_required()
    # def delete(self, uuid):
    #     """ Delete specific instance """
    #     if current_identity.roles not in ['super']:
    #         return pretty_response(403)
    #     options_instance = OptionsModel.query.get_or_404(uuid)
    #     try:
    #         options_instance.delete(options_instance)
    #         return pretty_response(20003)
    #     except SQLAlchemyError as e:
    #         current_app.logger.error(e)
    #         pretty_response(50001)
