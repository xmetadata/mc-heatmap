# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError

from common.utils import StandardResponse
from models.projects import ProjectsModel, ProjectsSchema
from models.dataset_rg_amount import DatasetAmountModel, DatasetAmountSchema
from models.dataset_rg_area import DatasetAreaModel, DatasetAreaSchema
from models.dataset_rg_none import DatasetNoneModel, DatasetNoneSchema
from models.dataset_rg_price import DatasetPriceModel, DatasetPriceSchema
from models.dataset_rg_room import DatasetRoomModel, DatasetRoomSchema

class Project(Resource):
    def __init__(self):
        self.param__ = {
            'table': '',
            'province': '',
            'city': '',
            'district': '',
            'starttm': '',
            'endtm': '',
            'stattype': '',
            'property': [],
            'interval': '',
        }

    def __RequestInstance(self, req):
        result = {}
        if not req:
            return None
        result['stattype'] = req['stattype'] if req.has_key('stattype') else None
        result['datetype'] = req['datetype'] if req.has_key('datetype') else None
        result['statdate'] = req['statdate'] if req.has_key('statdate') else None
        result['starttm']  = req['duration'][0] if req.has_key('duration') else None
        result['endtm']    = req['duration'][1] if req.has_key('duration') else None
        if req.has_key('scope'):
            result['province'] = req['scope'][0].split('.')[0]
            result['city'] = req['scope'][0].split('.')[1]
            result['district'] = req['scope'][0].split('.')[2]
        else:
            result['province'] = None
            result['city'] = None
            result['district'] = None
        result['property'] = req['property'] if req.has_key('property') else None
        result['arrange']  = req['arrange'] if req.has_key('arrange') else None
        result['intervals'] = req['intervals'] if req.has_key('intervals') else None
        return result

    def __GenerateParam(self, request, type):
        param = self.param__
        param['province'] = request['province']
        param['city'] = request['city']
        param['district'] = request['district']
        param['starttm'] = request['statdate']['from']
        param['endtm'] = request['statdate']['to']
        param['stattype'] = request['stattype']
        param['property'] = request['property']

        if type == 'amount':
            param['table'] = DatasetAmountModel
            for itr in request['interval']:
                param['interval'].append([itr.split(':')[0], itr.split(':')[1]])
        elif type == 'price':
            param['table'] = DatasetPriceModel
            for itr in request['interval']:
                param['interval'].append([itr.split(':')[0], itr.split(':')[1]])
        elif type == 'area':
            param['table'] = DatasetAreaModel
            for itr in request['interval']:
                param['interval'].append([itr.split(':')[0], itr.split(':')[1]])
        elif type == 'room':
            param['table'] = DatasetRoomModel
            param['interval'] = request['interval']
        elif type == 'none':
            param['table'] = DatasetNoneModel
            param['interval'] = None

    def __ProcessAmount(self, request):
        pass

    def __ProcessPrice(self, request):
        pass

    def __ProcessArea(self, request):
        param = self.__GenerateParam(request, DatasetAmountModel)
        result = ProjectsModel().query.join(param['table'].scope == param['district'],
                        param['table'].statdate.between(param['starttm'], param['endtm']),
                        param['table'].stattype == param['stattype'] == param['stattype']).all()
        if not result:
            return StandardResponse(500, 1, u'资源查找出错')
        projects = []
        for itr in result:
            if not itr.dataset_area:
                continue
            projects.append(itr)

    def __ProcessRoom(self, request):
        pass

    def __ProcessNone(self, request):
        pass

    @jwt_required()
    def get(self):
        req_data = request.get_json()
        result = self.__RequestInstance(req_data)
        if not result:
            return StandardResponse(404, 1, u'无效的请求数据')
        if result['arrange'] == u'amount':
            return self.__ProcessAmount(result)
        elif result['arrange'] == u'price':
            return self.__ProcessPrice(result)
        elif result['arrange'] == u'area':
            return self.__ProcessArea(result)
        elif result['arrange'] == u'room':
            return self.__ProcessRoom(result)
        elif result['arrange'] == None:
            return self.__ProcessNone(result)
        else:
            return StandardResponse(500, 1, u'无效的请求参数')

