# -*- coding: UTF-8 -*-
import json
import copy
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
            'arrange': '',
            'province': '',
            'city': '',
            'district': '',
            'datetype': '',
            'statdate': '',
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
            'count': 0.0
        }
        self.result__ = {
            'center': '',
            'zoom': '',
            'max': '',
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

    #请求参数格式化
    def __GenerateParam(self, request, data_type):
        param = copy.deepcopy(self.param__)
        param['province'] = request['province']
        param['city'] = request['city']
        param['district'] = request['district']
        param['datetype'] = request['datetype']
        if request['datetype'] in ['week', 'day']:
            param['starttm'] = request['starttm']
            param['endtm'] = request['endtm']
        else:
            param['statdate'] = request['statdate']
        param['stattype'] = request['stattype']
        param['property'] = request['property']
        param['arrange'] = request['arrange']

        if data_type in ['amount', 'price', 'area']:
            for itr in request['intervals']:
                split_list = itr.split(':')
                param['intervals'].append([int(split_list[0]), int(split_list[1])])
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
            if param['starttm'] and param['endtm']:
                filter.append(table.statdate.between(param['starttm'], param['endtm']))
        else:
            if param['statdate']:
                filter.append(table.statdate.like(param['statdate'] + '%'))
        if len(param['property']):
            filter.append(table.property.in_(param['property']))
        inter_list = []
        import pdb
        pdb.set_trace()
        if len(param['intervals']):
            if param['arrange'] in ['amount', 'price', 'area']:
                for itr in param['intervals']:
                    inter_list.append(table.arrange.between(itr[0], itr[1]))
                if len(inter_list):
                    filter.append(or_(*inter_list))
            else:
                inter_list.append(table.arrange.in_(param['intervals']))
                if len(inter_list):
                    filter.append(*inter_list)
        filters.append(and_(*filter))
        return filters

    #处理查询结果
    def __ProcessResult(self, result, stattype):
        if not result:
            return StandardResponse(404, 1, u'没有找到任何资源')
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
            project = copy.deepcopy(self.project__)
            project['name'] = itr.pro_name
            project['lat'] = itr.pro_lat
            project['lng'] = itr.pro_lng
            project['address'] = itr.pro_address
            project['count'] = count
            projects.append(project)
        if not len(projects):
            return StandardResponse(404, 1, u'没有找到任何资源')
        self.result__['data'] = projects
        return StandardResponse(200, 0, data = self.result__)

    def __ProcessAmount(self, request):
        param = self.__GenerateParam(request, 'amount')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetAmountModel, param)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        try:
            result = ProjectsModel().query.join(DatasetAmountModel).filter(*filters).all()
        except Exception, e:
            return StandardResponse(50001, 1, e.message)
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessPrice(self, request):
        param = self.__GenerateParam(request, 'price')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetPriceModel, param)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        result = ProjectsModel().query.join(DatasetPriceModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessArea(self, request):
        param = self.__GenerateParam(request, 'area')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetAreaModel, param)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        result = ProjectsModel().query.join(DatasetAreaModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessRoom(self, request):
        param = self.__GenerateParam(request, 'room')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetRoomModel, param)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        result = ProjectsModel().query.join(DatasetRoomModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    def __ProcessNone(self, request):
        param = self.__GenerateParam(request, 'none')
        if not param:
            return StandardResponse(401, 1, u'解析请求参数出错')
        filters = self.__GenerateFilters(DatasetNoneModel, param)
        if not len(filters):
            return StandardResponse(403, 1, u'查询数据库失败')
        result = ProjectsModel().query.join(DatasetNoneModel).filter(*filters).all()
        return self.__ProcessResult(result, param['stattype'])

    @jwt_required()
    def get(self):
        req_data = request.get_json()
        result = self.__RequestInstance(req_data)
        if not result:
            return StandardResponse(40001, 1, u'无效的请求数据')
        if result['arrange'] == u'amount':
            return self.__ProcessAmount(result)
        elif result['arrange'] == u'price':
            return self.__ProcessPrice(result)
        elif result['arrange'] == u'area':
            return self.__ProcessArea(result)
        elif result['arrange'] == u'room':
            return self.__ProcessRoom(result)
        elif result['arrange'] == u'none':
            return self.__ProcessNone(result)
        else:
            return StandardResponse(40001, 1, u'无效的请求数据')
