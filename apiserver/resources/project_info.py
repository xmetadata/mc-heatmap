# -*- coding: UTF-8 -*-
import json
import copy
import time
from datetime import datetime, timedelta

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
            'arrange': '',
            'province': '',
            'city': '',
            'district': '',
            'datetype': '',
            'statdate': '',
            'starttm': '',
            'endtm': '',
            'stattype': [],
            'property': '',
            'intervals': '',
        }
        self.stattype_map__ = {
            "sale": u"成交情况",
            "supply": u"上市情况",
            "stock": u"可售情况"
        }
        self.project__ = {
            'name': '',
            'lat': '',
            'lng': '',
            'address': '',
            'count': 0.0
        }
        self.result__ = {
            'max': 0.0,
            'data': []
        }

    #请求参数序列化
    def __RequestInstance(self, req):
        result = {}
        if not req:
            return None
        result['stattype'] = req['stattype'] if req.has_key('stattype') else None
        result['datetype'] = req['datetype'] if req.has_key('datetype') else None
        result['statdate'] = req['statdate'] if req.has_key('statdate') else None
        if req.has_key('scope'):
            result['province'] = None
            result['city'] = req['scope'][0]
            result['district'] = None if req['scope'][1] == '' else req['scope'][1]
        result['property'] = req['property'] if req.has_key('property') else None
        result['arrange']  = req['arrange'] if req.has_key('arrange') else None
        result['intervals'] = req['intervals'] if req.has_key('intervals') else None
        return result

    #请求参数格式化
    def __GenerateParam(self, request, data_type):
        param = copy.deepcopy(self.param__)
        param['province'] = request['province']
        param['city'] = request['city']
        param['district'] = request['district']
        param['datetype'] = request['datetype']
        if request['datetype'] in ['day']:
            param['starttm'] = request['statdate'][0]
            param['endtm'] = request['statdate'][1]
        else:
            if request['datetype'] == 'week':
                start_tm = time.strptime(request['statdate'], "%Y-%m-%d")
                param['starttm'] = request['statdate']
                end_tm = datetime(start_tm.tm_year, start_tm.tm_mon, start_tm.tm_mday) + timedelta(days=6)
                param['endtm'] = end_tm.strftime("%Y-%m-%d")
            elif request['datetype'] == 'month':
                start_tm = time.strptime(request['statdate'], "%Y-%m-%d")
                date_tm = datetime(start_tm.tm_year, start_tm.tm_mon, start_tm.tm_mday)
                param['statdate'] = date_tm.strftime("%Y-%m")
            else:
                start_tm = time.strptime(request['statdate'], "%Y-%m-%d")
                date_tm = datetime(start_tm.tm_year, start_tm.tm_mon, start_tm.tm_mday)
                param['statdate'] = date_tm.strftime("%Y")
        param['stattype'] = request['stattype']
        param['property'] = request['property']
        param['arrange'] = request['arrange']

        if data_type in ['amount', 'price', 'area']:
            param['intervals'] = request['intervals'].split(':')
        elif data_type == 'room':
            param['intervals'] = request['intervals']
        return param

    #sqlalchemy过滤器生成
    def __GenerateFilters(self, table, param):
        filters = []
        filter = []
        if param['city']:
            filter.append(table.city == param['city'])
        if param['district']:
            filter.append(table.scope == param['district'])
        if param['datetype'] in ['day', 'week']:
            filter.append(table.statdate.between(param['starttm'], param['endtm']))
        else:
            filter.append(table.statdate.like(param['statdate'] + '%'))
        if param['property']:
            filter.append(table.property == param['property'])
        if len(param['stattype']):
            stattype = self.stattype_map__[param['stattype'][0]]
            filter.append(table.stattype == stattype)
        inter = None
        if len(param['intervals']):
            if param['arrange'] in ['amount', 'price', 'area']:
                inter = table.arrange.between(param['intervals'][0], param['intervals'][1])
            else:
                inter = table.arrange == param['intervals']
            filter.append(inter)
        filters.append(and_(*filter))
        return filters

    #处理查询结果
    def __ProcessResult(self, result, stattype):
        if not result:
            return StandardResponse(200, 0, u'Found Nothing')
        projects = []
        max_project = 0.0
        for itr in result:
            if not itr.dataset_area:
                continue
            count = 0.0
            for dataset_itr in itr.dataset_area:
                if stattype[1] == u'amount':
                    count += float(dataset_itr.amount)
                elif stattype[1] == u'price':
                    count += float(dataset_itr.number)
                elif stattype[1] == u'area':
                    count += float(dataset_itr.area)
            if max_project < count:
                max_project = count
            project = copy.deepcopy(self.project__)
            project['name'] = itr.pro_name
            project['lat'] = itr.pro_lat
            project['lng'] = itr.pro_lng
            project['address'] = itr.pro_address
            project['count'] = count
            projects.append(project)
        if not len(projects):
            return StandardResponse(200, 0, u'Found Nothing')
        self.result__['data'] = projects
        self.result__['max'] = max_project
        return StandardResponse(200, 0, data = self.result__)

    def __ProcessAmount(self, request):
        param = self.__GenerateParam(request, 'amount')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetAmountModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        try:
            result = ProjectsModel().query.join(DatasetAmountModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessPrice(self, request):
        param = self.__GenerateParam(request, 'price')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetPriceModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = ProjectsModel().query.join(DatasetPriceModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessArea(self, request):
        param = self.__GenerateParam(request, 'area')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetAreaModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = ProjectsModel().query.join(DatasetAreaModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessRoom(self, request):
        param = self.__GenerateParam(request, 'room')
        if not param:
            return StandardResponse(400, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetRoomModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = ProjectsModel().query.join(DatasetRoomModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessNone(self, request):
        param = self.__GenerateParam(request, 'none')
        if not param:
            return StandardResponse(400, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetNoneModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = ProjectsModel().query.join(DatasetNoneModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    @jwt_required()
    def post(self):
        req_data = request.get_json()
        result = self.__RequestInstance(req_data)
        if not result:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        if result['arrange'] == u'amount':
            return self.__ProcessAmount(result)
        elif result['arrange'] == u'price':
            return self.__ProcessPrice(result)
        elif result['arrange'] == u'area':
            return self.__ProcessArea(result)
        elif result['arrange'] == u'room':
            return self.__ProcessRoom(result)
        else:
            return self.__ProcessNone(result)