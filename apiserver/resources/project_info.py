# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import current_app
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

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
            'province': '',
            'city': '',
            'district': '',
            'starttm': '',
            'endtm': '',
            'stattype': '',
            'property': [],
            'intervals': [],
        }
        self.project__ = {
            'name': '',
            'lat': '',
            'lng': '',
            'address': '',
            'count': ''
        }
        self.result__ = {
            'center': '',
            'zoom': '',
            'max': '',
            'data': []
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
        param['starttm'] = request['starttm']
        param['endtm'] = request['endtm']
        param['stattype'] = request['stattype']
        param['property'] = request['property']

        if type == 'amount' or type == 'price' or type == 'area':
            for itr in request['intervals']:
                split_list = itr.split(':')
                first = 0
                second = 0
                if len(split_list) == 1:
                    second = split_list[1]
                else:
                    first = split_list[0]
                    second = split_list[1]
                param['intervals'].append([first, second])
        elif type == 'room' or type == 'none':
            param['intervals'] = request['intervals']
        return param

    def __GenerateFilters(self, param, request):
        filters = []
        if param['city']:
            filters.append(DatasetAreaModel.city == param['city'])
        if param['district']:
            filters.append(DatasetAreaModel.scope == param['district'])
        if param['starttm'] and param['endtm']:
            filters.append(DatasetAreaModel.statdate.between(param['starttm'], param['endtm']))
        if len(param['property']):
            filters.append(DatasetAreaModel.property.in_(param['property']))
        if len(param['intervals']):
            inter_list = []
            for itr in param['intervals']:
                if request['stattype'] == u'sale':
                    inter_list.append(DatasetAreaModel.area.between(itr[0], itr[1]))
                elif request['stattype'] == u'price':
                    inter_list.append(DatasetAreaModel.amount.between(itr[0], itr[1]))
            if len(inter_list):
                filters.append(or_(*inter_list))
        return filters

    def __ProcessResult(self, result, stattype):
        if not result:
            return StandardResponse(500, 1, u'资源查找出错')
        projects = []
        for itr in result:
            if not itr.dataset_area:
                continue
            count = 0.0
            for dataset_itr in itr.dataset_area:
                if stattype == u'sale':
                    count += float(dataset_itr.area)
                elif stattype == u'price':
                    count += float(dataset_itr.amount)
            project = self.project__
            project['name'] = itr.pro_name
            project['lat'] = itr.pro_lat
            project['lng'] = itr.pro_lng
            project['address'] = itr.pro_address
            project['count'] = count
            projects.append(project)
        if not len(projects):
            return StandardResponse(404, 1, u'没有找到任何资源')
        self.result__['data'] = projects
        return StandardResponse(200, 0, self.result__)

    def __ProcessAmount(self, request):
        pass

    def __ProcessPrice(self, request):
        pass

    def __ProcessArea(self, request):
        param = self.__GenerateParam(request, 'area')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(param, request)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        import pdb
        pdb.set_trace()
        result = ProjectsModel().query.join(DatasetAreaModel).filter(*filters).all()
        return self.__ProcessResult(result)

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

