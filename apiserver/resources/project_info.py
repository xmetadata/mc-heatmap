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

from common.utils import StandardResponse, GetMonFirstLast
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
        if request['datetype'] in ['daterange']:
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
                first_day, last_day = GetMonFirstLast(start_tm.tm_year, start_tm.tm_mon)
                param['starttm'] = first_day.strftime("%Y-%m-%d")
                param['endtm'] = last_day.strftime("%Y-%m-%d")
            elif request['datetype'] == 'monthrange':
                start_tm = time.strptime(request['statdate'][0], "%Y-%m-%d")
                first_s, last_s = GetMonFirstLast(start_tm.tm_year, start_tm.tm_mon)
                param['starttm'] = first_s.strftime("%Y-%m-%d")
                end_tm = time.strptime(request['statdate'][1], "%Y-%m-%d")
                first_e, last_e = GetMonFirstLast(end_tm.tm_year, end_tm.tm_mon)
                param['endtm'] = last_e.strftime("%Y-%m-%d")
            else:
                date_tm = time.strptime(request['statdate'], "%Y-%m-%d")
                start_tm = datetime(date_tm.tm_year, 1, 1)
                end_tm = datetime(date_tm.tm_year, 12, 31)
                param['starttm'] = start_tm.strftime("%Y-%m-%d")
                param['endtm'] = end_tm.strftime("%Y-%m-%d")
        param['stattype'] = request['stattype']
        param['property'] = request['property']
        param['arrange'] = request['arrange']

        if data_type in ['amount', 'price', 'area']:
            split_list = request['intervals'].split(':')
            if len(split_list[0]) == 0:
                split_list[0] = 0
            elif len(split_list[1]) == 0:
                split_list[1] = 3000000
            param['intervals'] = split_list
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
        if param['datetype'] in ['daterange', 'week']:
            filter.append(table.datetype == 'day')
        elif param['datetype'] in ['monthrange', 'month', 'year']:
            filter.append(table.datetype == 'month')
        else:
            filter.append(table.datetype == 'month')
        if param['starttm'] and param['endtm']:
            filter.append(table.statdate >= param['starttm'])
            filter.append(table.statdate <= param['endtm'])
        if param['property']:
            filter.append(table.property == param['property'])
        if len(param['stattype']) != 0:
            stattype = self.stattype_map__[param['stattype'][0]]
            filter.append(table.stattype == stattype)
        if len(param['intervals']) != 0:
            if param['arrange'] in ['amount', 'price', 'area']:
                filter.append(table.intervals >= int(param['intervals'][0]))
                filter.append(table.intervals < int(param['intervals'][1]))
            else:
                filter.append(table.intervals == param['intervals'])
        filters.append(and_(*filter))
        return filters

    #处理查询结果
    def __ProcessResult(self, result, param):
        if not result:
            return StandardResponse(200, 0, u'Found Nothing')
        projects_map = {}
        max_project = 0.0
        for itr in result:
            try:
                if itr.project.pro_name in projects_map:
                    projects_map[itr.project.pro_name]['amount'] += itr.amount
                    projects_map[itr.project.pro_name]['area'] += itr.area
                    projects_map[itr.project.pro_name]['number'] += itr.number
                else:
                    statistic = {
                        'address' : itr.project.pro_address,
                        'lat' : float(itr.project.pro_lat) if itr.project.pro_lat else 0.0,
                        'lng' : float(itr.project.pro_lng) if itr.project.pro_lng else 0.0,
                        'amount' : itr.amount,
                        'area' : itr.area,
                        'number' : itr.number
                    }
                    projects_map[itr.project.pro_name] = statistic
            except Exception, e:
                return StandardResponse(500, 1, e.message)
        del result
        projects = []
        try:
            for name, stat in projects_map.items():
                project = copy.deepcopy(self.project__)
                project['name'] = name
                project['address'] = stat['address']
                project['lat'] = stat['lat']
                project['lng'] = stat['lng']
                count = 0.0
                if param['stattype'][1] == u'amount':
                    count = stat['amount']
                elif param['stattype'][1] == u'price':
                    count = int(stat['amount'] * 10000 / stat['area']) if stat['area'] != 0 else 0
                elif param['stattype'][1] == u'area':
                    count = stat['area']
                elif param['stattype'][1] == u'number':
                    count = stat['number']
                if max_project < count:
                    max_project = count
                project['count'] = count
                projects.append(project)
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        if len(projects) == 0:
            return StandardResponse(200, 0, u'Found Nothing')
        result = copy.deepcopy(self.result__)
        result['data'] = projects
        result['max'] = max_project
        return StandardResponse(200, 0, data = result)

    def __ProcessAmount(self, request):
        param = self.__GenerateParam(request, 'amount')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetAmountModel, param)
        if len(filters) == 0:
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = None
        try:
            result = DatasetAmountModel().query.join(ProjectsModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param)

    def __ProcessPrice(self, request):
        param = self.__GenerateParam(request, 'price')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetPriceModel, param)
        if len(filters) == 0:
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = None
        try:
            result = DatasetPriceModel().query.join(ProjectsModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param)

    def __ProcessArea(self, request):
        param = self.__GenerateParam(request, 'area')
        if not param:
            return StandardResponse(400, 1, u'Invalid Request Parameters')
        filters = self.__GenerateFilters(DatasetAreaModel, param)
        if len(filters) == 0:
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = None
        try:
            result = DatasetAreaModel().query.join(ProjectsModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param)

    def __ProcessRoom(self, request):
        param = self.__GenerateParam(request, 'room')
        if not param:
            return StandardResponse(400, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetRoomModel, param)
        if len(filters) == 0:
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = None
        try:
            result = DatasetRoomModel().query.join(ProjectsModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param)

    def __ProcessNone(self, request):
        param = self.__GenerateParam(request, 'none')
        if not param:
            return StandardResponse(400, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetNoneModel, param)
        if not len(filters):
            return StandardResponse(500, 1, u'SQLAlchemy Error')
        result = None
        try:
            result = DatasetNoneModel().query.join(ProjectsModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(500, 1, e.message)
        return self.__ProcessResult(result, param)

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
